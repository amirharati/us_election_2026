import sys
from pathlib import Path
import tempfile
import unittest
import nbformat
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from notebook_sources import manage, check_source, save_execution

class NotebookRecoveryTests(unittest.TestCase):
    def test_conflict_preserves_edits_and_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'notebooks/12_test.ipynb';p.parent.mkdir()
            n=nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell('1')])
            nbformat.write(n,p);original=p.read_bytes()
            p.write_bytes(original+b'\n')
            with self.assertRaisesRegex(RuntimeError,'changed during execution'):
                save_execution(p,n,original)
            self.assertEqual(p.read_bytes(),original+b'\n')
            copies=list((Path(tmp)/'cache/notebook_history/12_test').glob('*executed.ipynb'))
            self.assertEqual(len(copies),1)
            self.assertEqual(nbformat.read(copies[0],4).cells[0].source,'1')

    def test_restore_and_normal_save(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'notebooks/12_test.ipynb';p.parent.mkdir()
            n=nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell('1')])
            nbformat.write(n,p);manage(p)
            n.cells[0].source='2';nbformat.write(n,p)
            with self.assertRaises(ValueError): check_source(p,n)
            backup=manage(p,restore=True)
            self.assertEqual(nbformat.read(backup,4).cells[0].source,'2')
            restored=nbformat.read(p,4);check_source(p,restored)
            restored.cells[0].execution_count=1
            copy=save_execution(p,restored,p.read_bytes())
            self.assertEqual(p.read_bytes(),copy.read_bytes())
