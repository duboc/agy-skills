"""Verify template dry runs never invoke the cloud CLI. Requires Bash."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class TemplateTests(unittest.TestCase):
    def test_inspection_failure_does_not_create_account(self):
        bash = os.environ.get('BASH_EXECUTABLE') or shutil.which('bash')
        if not bash:
            self.skipTest('Bash is unavailable')
        script = Path(__file__).resolve().parents[1] / 'assets/init-gcp-template.sh'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            log = root / 'calls.txt'
            env_file = root / 'bash-env.sh'
            env_file.write_text('gcloud() { echo "$*" >> "$CALL_LOG"; '
                                'if [ "$1" = billing ]; then echo True; return 0; fi; '
                                'return 2; }\n', encoding='utf-8')
            env = dict(os.environ, DRY_RUN='false', PROJECT_ID='fixture-project',
                       CALL_LOG=log.as_posix(), BASH_ENV=env_file.as_posix())
            result = subprocess.run([bash, script.as_posix()], env=env,
                                    capture_output=True, text=True, timeout=10)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn('create', log.read_text())

    def test_dry_run_does_not_invoke_gcloud(self):
        bash = os.environ.get('BASH_EXECUTABLE') or shutil.which('bash')
        if not bash:
            self.skipTest('Bash is unavailable')
        script = Path(__file__).resolve().parents[1] / 'assets/init-gcp-template.sh'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            log = root / 'calls.txt'
            env_file = root / 'bash-env.sh'
            env_file.write_text('gcloud() { echo called >> "$CALL_LOG"; return 1; }\n', encoding='utf-8')
            env = dict(os.environ, DRY_RUN='true', PROJECT_ID='fixture-project',
                       CALL_LOG=log.as_posix(), BASH_ENV=env_file.as_posix())
            result = subprocess.run([bash, script.as_posix()], env=env,
                                    capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(log.exists(), 'Dry run invoked gcloud')
            self.assertIn('DRY RUN', result.stdout)


if __name__ == '__main__':
    unittest.main()
