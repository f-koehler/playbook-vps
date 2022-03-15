DEBUG = False
EMAIL_HOST = "{{ bot.email.smtp.host }}"
EMAIL_HOST_PASSWORD = "{{ bot.email.password }}"
EMAIL_HOST_USER = "{{ bot.email.address }}"
EMAIL_PORT = "{{ bot.email.smtp.port }}"
EMAIL_USE_TLS = True
MATRIX_ACCESS_TOKEN = "{{ bot.matrix.token }}"
MATRIX_HOMESERVER = "{{ bot.matrix.homeserver }}"
MATRIX_USER_ID = "{{ bot.matrix.user }}"
ALLOWED_HOSTS = [{% for host in healthchecks.allowed_hosts %}
    "{{ host }}",
{% endfor %}]
CSRF_TRUSTED_ORIGINS = [{% for host in healthchecks.allowed_hosts %}
    "https://{{ host }}",
{% endfor %}]
SITE_NAME = "{{ healthchecks.site.name }}"
SITE_ROOT = "{{ healthchecks.site.root }}"
REGISTRATION_OPEN = False