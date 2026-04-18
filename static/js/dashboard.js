async function updateStatus(taskCode, newStatus) {
  try {
    const response = await fetch(`/api/update-status/${taskCode}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    });

    const data = await response.json();

    if (data.success) {
      // Update the status badge
      const badge = document.getElementById(`status-${taskCode}`);
      badge.className = `status-badge status-${newStatus}`;
      const labels = {
        'pending': 'Pending',
        'in_progress': 'In Progress',
        'completed': 'Completed'
      };
      badge.textContent = labels[newStatus];

      // Flash the row green briefly
      const row = document.getElementById(`row-${taskCode}`);
      row.style.background = '#e9fbe9';
      setTimeout(() => { row.style.background = ''; }, 1000);
    }
  } catch (error) {
    alert('Failed to update status. Please try again.');
  }
}