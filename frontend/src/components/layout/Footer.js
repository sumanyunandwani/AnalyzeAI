import React from 'react';
import { Box, Container, Stack, IconButton } from '@mui/material';
import { YouTube, Twitter, Email, Instagram } from '@mui/icons-material';

const socialLinks = [
  {
    name: 'YouTube',
    icon: YouTube,
    url: 'https://youtube.com',
    hoverColor: '#FF0000'
  },
  {
    name: 'Twitter',
    icon: Twitter,
    url: 'https://twitter.com',
    hoverColor: '#1DA1F2'
  },
  {
    name: 'Email',
    icon: Email,
    url: 'mailto:contact@example.com',
    hoverColor: '#EA4335'
  },
  {
    name: 'Instagram',
    icon: Instagram,
    url: 'https://instagram.com',
    hoverColor: null, // Special gradient handling
  }
];

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 2,
        px: 2,
        mt: 'auto',
        background: 'rgba(0, 0, 0, 0.1)',
        backdropFilter: 'blur(10px)',
        borderTop: '1px solid rgba(255, 255, 255, 0.2)'
      }}
    >
      <Container maxWidth="sm">
        <Stack
          direction="row"
          spacing={2}
          justifyContent="center"
          alignItems="center"
        >
          {socialLinks.map((social) => {
            const Icon = social.icon;
            const baseStyles = {
              color: 'white',
              backgroundColor: 'rgba(255, 255, 255, 0.1)',
              backdropFilter: 'blur(10px)',
              transition: 'all 0.3s ease',
              p: 1,
              '&:hover': {
                transform: 'translateY(-3px)',
                ...(social.name === 'Instagram' 
                  ? {
                      background: 'linear-gradient(135deg, #F58529 0%, #DD2A7B 50%, #8134AF 100%)',
                      boxShadow: '0 5px 15px rgba(221, 42, 123, 0.4)'
                    }
                  : {
                      backgroundColor: social.hoverColor,
                      boxShadow: `0 5px 15px ${social.hoverColor}40`
                    }
                )
              }
            };

            return (
              <IconButton
                key={social.name}
                aria-label={social.name}
                href={social.url}
                target="_blank"
                sx={baseStyles}
              >
                <Icon fontSize="medium" />
              </IconButton>
            );
          })}
        </Stack>
      </Container>
    </Box>
  );
};

export default Footer;
