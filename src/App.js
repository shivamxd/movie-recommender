import React, { useState } from 'react';

function App() {
  const [input, setInput] = useState('');  // User input state
  const [responseData, setResponseData] = useState(null); // API response state
  const [loading, setLoading] = useState(false); // Loading indicator

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: input }),
      });

      const data = await response.json(); // Parse JSON response
      setResponseData(data); // Set response data
    } catch (error) {
      console.error('Error:', error);
      setResponseData({ error: 'Failed to fetch data' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '50px', fontFamily: 'Arial' }}>
      <h1>Enter Movie Name</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter some text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{ padding: '10px', width: '300px', marginRight: '10px' }}
        />
        <button type="submit" style={{ padding: '10px' }}>Send</button>
      </form>

      {loading && <p>Loading...</p>}

      {responseData && (
        <div style={{ marginTop: '20px' }}>
          <h3>Recommendations:</h3>
          <pre style={{ background: '#f4f4f4', padding: '10px' }}>
            {JSON.stringify(responseData, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;
