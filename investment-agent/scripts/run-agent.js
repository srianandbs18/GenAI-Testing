const { spawn } = require('child_process');
const path = require('path');
const os = require('os');
const fs = require('fs');

const isWindows = os.platform() === 'win32';
const agentDir = path.join(__dirname, '..', 'agent');
// Check for both .venv and venv (Windows might use venv)
let venvDir = path.join(agentDir, isWindows ? 'venv' : '.venv');
if (!fs.existsSync(venvDir)) {
  // Try the other one
  venvDir = path.join(agentDir, isWindows ? '.venv' : 'venv');
}
const venvPython = isWindows 
  ? path.join(venvDir, 'Scripts', 'python.exe')
  : path.join(venvDir, 'bin', 'python');

const agentScript = path.join(agentDir, 'agent.py');

console.log(`Starting agent from: ${agentDir}`);
console.log(`Using Python: ${venvPython}`);

const pythonProcess = spawn(venvPython, [agentScript], {
  cwd: agentDir,
  stdio: 'inherit',
  shell: isWindows
});

pythonProcess.on('error', (error) => {
  console.error(`Failed to start agent: ${error.message}`);
  console.error(`Make sure the virtual environment exists at: ${path.dirname(venvPython)}`);
  process.exit(1);
});

pythonProcess.on('exit', (code) => {
  if (code !== 0) {
    console.error(`Agent exited with code ${code}`);
    process.exit(code);
  }
});

