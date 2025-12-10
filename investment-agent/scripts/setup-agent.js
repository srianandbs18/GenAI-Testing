const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

const isWindows = os.platform() === 'win32';
const agentDir = path.join(__dirname, '..', 'agent');
const venvDir = isWindows 
  ? path.join(agentDir, 'venv')
  : path.join(agentDir, '.venv');

console.log('Setting up agent environment...');
console.log(`Agent directory: ${agentDir}`);
console.log(`Virtual environment: ${venvDir}`);

// Check if venv exists
if (!fs.existsSync(venvDir)) {
  console.log('Creating virtual environment...');
  try {
    execSync(`python -m venv ${venvDir}`, { stdio: 'inherit', cwd: agentDir });
    console.log('Virtual environment created successfully!');
  } catch (error) {
    console.error('Failed to create virtual environment:', error.message);
    process.exit(1);
  }
} else {
  console.log('Virtual environment already exists.');
}

// Install requirements
const requirementsFile = path.join(agentDir, 'requirements.txt');
if (fs.existsSync(requirementsFile)) {
  console.log('Installing Python dependencies...');
  const pip = isWindows
    ? path.join(venvDir, 'Scripts', 'pip.exe')
    : path.join(venvDir, 'bin', 'pip');
  
  try {
    execSync(`${pip} install -r ${requirementsFile}`, { stdio: 'inherit', cwd: agentDir });
    console.log('Dependencies installed successfully!');
  } catch (error) {
    console.error('Failed to install dependencies:', error.message);
    process.exit(1);
  }
} else {
  console.log('No requirements.txt found, skipping dependency installation.');
}

console.log('Agent setup complete!');

