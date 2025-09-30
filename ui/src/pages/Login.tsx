import { useState } from "react";
import {
  Avatar,
  Button,
  TextField,
  Box,
  Typography,
  Container,
  CssBaseline,
  Paper,
  CircularProgress
} from "@mui/material";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false); // ✅ Loading state
  const navigate = useNavigate();

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    setLoading(true); // start loading

    try {
      const params = new URLSearchParams();
      params.append("username", email);
      params.append("password", password);

      const response = await axios.post("http://localhost:8000/token", params, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      const { access_token } = response.data;
      localStorage.setItem("token", access_token);
      console.log("Token saved:", access_token);
      navigate("/chat");
    } catch (err: any) {
      console.error(err);
      setError("Login failed. Check email and password.");
    } finally {
      setLoading(false); // stop loading
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <Paper
        elevation={6}
        sx={{ p: 4, mt: 8, display: "flex", flexDirection: "column", alignItems: "center", borderRadius: 3 }}
      >
        <Avatar sx={{ m: 1, bgcolor: "primary.main" }}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign in
        </Typography>
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            label="Email Address"
            autoComplete="email"
            autoFocus
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            label="Password"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {error && (
            <Typography color="error" variant="body2" sx={{ mt: 1 }}>
              {error}
            </Typography>
          )}
          <Button
            type="submit"
            fullWidth
            variant="contained"
            disabled={loading} // ✅ Disable while loading
            sx={{ mt: 3, mb: 2, borderRadius: 2, position: "relative" }}
          >
            {loading ? (
              <CircularProgress size={24} color="inherit" /> // ✅ Show spinner
            ) : (
              "Sign In"
            )}
          </Button>
        </Box>
      </Paper>
    </Container>
  );
}
