import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Avatar,
  Menu,
  MenuItem,
  IconButton,
  Divider,
  CircularProgress
} from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';
import LogoutIcon from '@mui/icons-material/Logout';
import { useAuth } from '../auth/AuthContext';
import LoginDialog from '../auth/LoginDialog';

const Header = () => {
  const { user, logout, isAuthenticated, loading } = useAuth();
  const [loginOpen, setLoginOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    handleMenuClose();
  };

  // Debug logging
  console.log('Header - Auth State:', { user, isAuthenticated, loading });

  return (
    <>
      <AppBar
        position="static"
        elevation={0}
        sx={{
          backgroundColor: 'transparent',
          backdropFilter: 'blur(10px)',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
        }}
      >
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          {/* Left side - Welcome message */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Typography
              variant="h6"
              sx={{
                color: 'white',
                fontWeight: 600,
                textShadow: '0 2px 4px rgba(0,0,0,0.1)'
              }}
            >
              Hi, {loading ? '...' : (isAuthenticated && user ? user.name : 'Guest')}
            </Typography>
          </Box>

          {/* Right side - Login/User menu */}
          <Box>
            {loading ? (
              <CircularProgress size={30} sx={{ color: 'white' }} />
            ) : isAuthenticated && user ? (
              <>
                <IconButton
                  onClick={handleMenuOpen}
                  sx={{
                    p: 0.5,
                    '&:hover': {
                      backgroundColor: 'rgba(255, 255, 255, 0.1)'
                    }
                  }}
                >
                  <Avatar
                    sx={{
                      width: 40,
                      height: 40,
                      bgcolor: 'rgba(255, 255, 255, 0.2)',
                      border: '2px solid rgba(255, 255, 255, 0.3)'
                    }}
                  >
                    {user.name.charAt(0).toUpperCase()}
                  </Avatar>
                </IconButton>
                
                <Menu
                  anchorEl={anchorEl}
                  open={Boolean(anchorEl)}
                  onClose={handleMenuClose}
                  PaperProps={{
                    sx: {
                      mt: 1.5,
                      minWidth: 200,
                      '& .MuiMenuItem-root': {
                        px: 2,
                        py: 1
                      }
                    }
                  }}
                  transformOrigin={{ horizontal: 'right', vertical: 'top' }}
                  anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
                >
                  <Box sx={{ px: 2, py: 1.5 }}>
                    <Typography variant="subtitle2" fontWeight={600}>
                      {user.name}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {user.email}
                    </Typography>
                  </Box>
                  <Divider />
                  <MenuItem onClick={handleMenuClose}>
                    <PersonIcon fontSize="small" sx={{ mr: 1.5 }} />
                    Profile
                  </MenuItem>
                  <MenuItem onClick={handleLogout}>
                    <LogoutIcon fontSize="small" sx={{ mr: 1.5 }} />
                    Logout
                  </MenuItem>
                </Menu>
              </>
            ) : (
              <Button
                variant="contained"
                onClick={() => setLoginOpen(true)}
                sx={{
                  backgroundColor: 'rgba(255, 255, 255, 0.2)',
                  color: 'white',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  textTransform: 'none',
                  px: 3,
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.3)',
                    borderColor: 'rgba(255, 255, 255, 0.4)'
                  }
                }}
              >
                Login
              </Button>
            )}
          </Box>
        </Toolbar>
      </AppBar>

      <LoginDialog
        open={loginOpen}
        onClose={() => setLoginOpen(false)}
      />
    </>
  );
};

export default Header;
