import React, { useState } from 'react';
import {
  Container,
  Box,
  TextField,
  Button,
  Paper,
  Typography,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';

function App() {
  const [mediaPath, setMediaPath] = useState('');
  const [videoFile, setVideoFile] = useState('');
  const [audioFile, setAudioFile] = useState('');
  const [messages, setMessages] = useState([]);
  const [blogPost, setBlogPost] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessages([]);
    setBlogPost('');

    try {
      const response = await fetch('http://localhost:8000/process-media', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          media_path: mediaPath,
          video_file: videoFile,
          audio_file: audioFile,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'An error occurred');
      }

      setMessages(data.messages);
      setBlogPost(data.blog_post);
    } catch (error) {
      setMessages([`Error: ${error.message}`]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Media Processor
        </Typography>

        <Paper sx={{ p: 3, mb: 3 }}>
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Media Files Location"
              value={mediaPath}
              onChange={(e) => setMediaPath(e.target.value)}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Video File Name"
              value={videoFile}
              onChange={(e) => setVideoFile(e.target.value)}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Audio File Name"
              value={audioFile}
              onChange={(e) => setAudioFile(e.target.value)}
              margin="normal"
              required
            />
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={loading}
              sx={{ mt: 2 }}
            >
              {loading ? <CircularProgress size={24} /> : 'Start Generation'}
            </Button>
          </form>
        </Paper>

        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Process Messages
          </Typography>
          <List>
            {messages.map((message, index) => (
              <ListItem key={index}>
                <ListItemText primary={message} />
              </ListItem>
            ))}
          </List>
        </Paper>

        {blogPost && (
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Generated Blog Post
            </Typography>
            <Typography component="div" sx={{ whiteSpace: 'pre-wrap' }}>
              {blogPost}
            </Typography>
          </Paper>
        )}
      </Box>
    </Container>
  );
}

export default App; 