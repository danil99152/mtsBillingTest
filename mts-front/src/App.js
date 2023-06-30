import React, { useState } from 'react';
import axios from 'axios';
import { Typography, Box, Button, CircularProgress } from '@mui/material';

function App() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post('http://127.0.0.1:8000/process-cdr-file/', formData);
      setResponse(response.data);
      console.log(response.data)
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
      <Box sx={{ padding: '2rem', textAlign: 'center' }}>
        <Typography variant="h4" component="h1" gutterBottom>
          MTS minibilling
        </Typography>
        <form onSubmit={handleSubmit}>
          <input type="file" onChange={handleFileChange} />
          <Button type="submit" variant="contained" disabled={isLoading}>
            Upload
          </Button>
        </form>

        {isLoading && <CircularProgress sx={{ margin: '2rem 0' }} />}

        {response && (
            <Box sx={{ marginTop: '2rem' }}>
              <Typography variant="h5" component="h2" gutterBottom>
                Пара префиксных зон и сумма длительности секунд разговоров:
              </Typography>
              {Object.entries(response).map(([key, value]) => (
                  <Typography variant="body1" gutterBottom key={key}>
                    {key}: {value}
                  </Typography>
              ))}
            </Box>
        )}
      </Box>
  );
}

export default App;
