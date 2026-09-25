"""Migrate public output copies to compact storage without deleting local files."""
from pathlib import Path
import json
import hashlib
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import election_lab as lab
from output_publication import compact_bundle,replace_directory,write_index


def migrate(root):
    root=Path(root)
    for old,new in [('outputs/results/forecast/live_reports','outputs/reports/forecast'),
                    ('outputs/results/markets/polymarket','outputs/reports/markets/polymarket')]:
        source=root/old;dest=root/new
        # Existing canonical bundles take precedence once migration is complete.
        if source.exists() and not (dest/'manifest.json').exists():replace_directory(source,dest)
    # Original manifests are verified first. Re-seal only copies whose format changes.
    for manifest in sorted((root/'outputs').rglob('manifest.json')):
        directory=manifest.parent
        if directory.is_relative_to(root/'outputs/results/forecast/live_reports') or directory.is_relative_to(root/'outputs/results/markets'):continue
        lab.verify_run(directory)
        compact_bundle(directory,live=directory==root/'outputs/results/forecast/live')
    for report in (root/'outputs/reports/history').glob('*/*'):
        if report.is_dir():compact_bundle(report)
    directory=root/'outputs/reports/forecast'
    for p in directory.glob('*.md'):
        p.write_text(p.read_text().replace('../../results/forecast/live_reports/','./'))
    if (directory/'manifest.json').exists():
        (directory/'manifest.json').write_text(json.dumps({str(p.relative_to(directory)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(directory.rglob('*')) if p.is_file() and p.name!='manifest.json'},indent=2)+'\n')
    write_index(root)


if __name__=='__main__':migrate(lab.ROOT)
