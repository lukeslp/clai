# LOCAL clones anywhere under $HOME
find "$HOME" -type d -name 'chainliit*' -exec printf '%s\n' {} +

# (alternate spelling)
find "$HOME" -type d -name 'chainlit*'  -exec printf '%s\n' {} +

# GITHUB repos in your account (requires gh + jq)
gh repo list coolhand --limit 1000 --json name \
  | jq -r '.[] | .name' \
  | grep -E '^chainliit|^chainlit'