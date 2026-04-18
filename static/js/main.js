async function sendRequest() {
  const input = document.getElementById('userInput');
  const text = input.value.trim();
  if (!text) return;

  // Show user message in chat
  const chatBox = document.getElementById('chatBox');
  const userMsg = document.createElement('div');
  userMsg.className = 'message user-message';
  userMsg.textContent = text;
  chatBox.appendChild(userMsg);
  input.value = '';

  // Show loading
  document.getElementById('loading').classList.add('active');
  document.getElementById('resultCard').style.display = 'none';
  document.getElementById('sendBtn').disabled = true;

  try {
    const response = await fetch('/api/process/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });

    const data = await response.json();
    
    if (!response.ok) {
      alert('Server error: ' + (data.error || 'Unknown error'));
      return;
    }
    
    displayResult(data);

  } catch (error) {
    console.error('Error:', error);
    alert('Error: ' + error.message);  } finally {
    document.getElementById('loading').classList.remove('active');
    document.getElementById('sendBtn').disabled = false;
  }
}

function displayResult(data) {
  // Task meta
  document.getElementById('taskMeta').innerHTML = `
    <div class="meta-item">
      <div class="meta-label">Task Code</div>
      <div class="meta-value">${data.task_code}</div>
    </div>
    <div class="meta-item">
      <div class="meta-label">Intent</div>
      <div class="meta-value">${data.intent.replace('_', ' ')}</div>
    </div>
    <div class="meta-item">
      <div class="meta-label">Risk Score</div>
      <div class="meta-value risk-${data.risk_label}">${data.risk_score}/100 (${data.risk_label})</div>
    </div>
    <div class="meta-item">
      <div class="meta-label">Assigned To</div>
      <div class="meta-value">${data.assigned_team}</div>
    </div>
  `;

  // Steps
  const stepsList = document.getElementById('taskSteps');
  stepsList.innerHTML = '';
  data.steps.forEach(step => {
    const li = document.createElement('li');
    li.textContent = step;
    stepsList.appendChild(li);
  });

  // Messages
  document.getElementById('msgWhatsapp').textContent = data.messages.whatsapp;
  document.getElementById('msgEmail').textContent = data.messages.email;
  document.getElementById('msgSms').textContent = data.messages.sms;

  // Show card
  document.getElementById('resultCard').style.display = 'block';
  document.getElementById('resultCard').scrollIntoView({ behavior: 'smooth' });
}

// Allow Enter key to send (Shift+Enter for new line)
document.getElementById('userInput').addEventListener('keydown', function(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendRequest();
  }
});