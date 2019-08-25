Updating Daily Email Test Reports
==========

Currently, there is one VM provisioned to run a daily end-to-end test for the klee-web server and send a report via email. 

## Update Email Recipient
To update the email recipient open the file `src/klee_web/tests/automated_e2e_tests.py`.  

Find the line which assignes a Python list to the `receivers_email` variable.
```bash
receivers_email = ["denis.gavrielov18@ic.ac.uk"]
```
Add or delete recipients from this list.

Finally, provision the testing machine as illustrated in the DEPLOY.md file.

## Update Sender Email and Password
Currently the sender email is specified on this line:
```bash
sender_email = "klee.tests@gmail.com"
```
klee.tests@gmail.com is a gmail account which was created purely for the daily automated test report. This account can be replaced, but keep in mind to possibly change security settings to allow the Python script to log onto the account.

The password is added through the environmental variable GMAIL_PASSWORD which is securely stored in the ansible vault. To update the password, first update it in the email account and then update the ansible vault password.

First, open the secrets file with the ansible vault command:
```bash
ansible-vault edit --vault-password-file=~/.klee_vault_password provisioning/vars/secrets.yml
```
Make sure to place the .klee_vault_password file into your home directory. You can acquire this file from the current maintainers of the website. This command will encrypt and open the `secrets.yml` file and any changes to the variables will overwrite this file. 

If you simply want to view the password for the gmail account you can use the `ansible-vault view` command to do so without the risk of changing variables:
```bash
ansible-vault view --vault-password-file=~/.klee_vault_password provisioning/vars/secrets.yml
```

Finally, provision the testing machine as illustrated in the DEPLOY.md file.

## Update Date and Time of automated tests

To update the configuration of the cron job the provisioning has to be updated. The file `provisioning/roles/e2e-tests/tasks/main.yml` holds the provisioning task to install the cronjob. Currently named "Add cronjob for automated tests daily at 2pm", this task can be modified to any typical cronjob setting. 

```yml
- name: Add cronjob for automated tests daily at 2pm
  cron:
    name: "Test Klee Web"
    minute: "0"
    hour: "14"
    job: "/src/python_runner.sh /usr/bin/python3 /titb/src/klee_web/tests/automated_e2e_tests.py"
    user: "{{ 'dg3718' if (not development) else 'vagrant' }}"
  when: not ci
```
For example, you can change the hour setting to receive the email at a different time of the day. Other options can be explored from the [official Ansible cron documentation](https://docs.ansible.com/ansible/latest/modules/cron_module.html).

Finally, provision the testing machine as illustrated in the DEPLOY.md file.


Continuous Website Availability Alerts
=========
The test reports are essential to check the functionality of the website. However, they are designed to inform the maintainer of the website only once a day. To get more up-to-date alerts a monitoring service was set up. 

**UptimeRobot** is a free monitoring service which pings the web address every 5 minutes and sends an email alert if the site did not respond. It then pings the site every 5 minutes again and sends an email update once the site responds again. 

Again, this does not test if the website functionalities are working as expected, but it does check the status of the website overall.

To add or remove yourself from the email list, you need to first obtain the password for the account with:

```bash
ansible-vault view --vault-password-file=~/.klee_vault_password provisioning/vars/secrets.yml
```

Get the `uptimerobot_password`. Visit https://uptimerobot.com/ and log in with the email address `klee.tests@gmail.com` and the password from the Ansible Vault file. 

Under `My Settings` you can add or remove Alert Contacts by simply adding the email address onto which you want to receive the emails for.

Here you also have a dashboard to check the availability of the web server for up to the past 30 days.
