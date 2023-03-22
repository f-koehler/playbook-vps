# Protonmail login

1. Stop container:
   ```bash
   docker stop paperless_protonmail
   ```
2. Run init command:
   ```bash
   docker run --rm -it -v paperless_protonmail:/root  paperless_protonmail init
   ```
3. Type `login` and follow the prompts.
4. Wait for the sync to complete.
5. Type `info` to obtain IMAP/SMTP config.
6. Type `exit` to leave ProtonMail CLI.
7. Start container:
   ```bash
   docker start paperless_protonmail
   ```

# Pi-hole Recursive DNS

Set the upstream DNS server to `127.0.0.1#5335`.
