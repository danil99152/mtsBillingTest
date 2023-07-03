import React, { useState } from 'react';
import { Typography, Box, TextField, Button, Paper, CircularProgress } from '@mui/material';

const App = () => {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);

    if (file) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('http://127.0.0.1:8000/process-cdr-file/', {
          method: 'POST',
          body: formData,
        });

        const data = await response.json();
        setResponse(data);
      } catch (error) {
        console.error('Error:', error);
      } finally {
      setIsLoading(false);
      }
    }
  }

  return (
      <Box sx={{ padding: '2rem', textAlign: 'left' }}>
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
            <Paper elevation={3} style={{ padding: '20px', margin: '20px' }}>
              <h2>Суммы секунд для префиксных зон:</h2>
              {Object.entries(response).map(([key, value]) => (
                  <TextField
                      key={key}
                      label={key}
                      value={value}
                      fullWidth
                      margin="normal"
                      variant="outlined"
                  />
              ))}
            </Paper>
        )}
      </Box>
  );
};

export default App;
