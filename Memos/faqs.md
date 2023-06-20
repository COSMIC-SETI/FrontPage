# COSMIC FAQs

## Creating New User Accounts (Head Node only)

1. obtain the `$username` desired by the new user, and a public SSH key
2. On `cosmic-head`:

```
sudo adduser $username
sudo mkdir ~$username/.ssh
sudo vim ~$username/.ssh/authorized_keys
# Paste the public SSH key in this file
sudo chown $username:$username ~$username/.ssh/authorized_keys
sudo chmod 600 ~$username/.ssh/authorized_keys
```

