---
title: "CAPTCHA/reCAPTCHA"
date: 2023-06-15T13:07:30+01:00
draft: false
---

# CAPTCHA

* CAPTCHAs can be required on sign-up to verify the human-ness of a potential user.
* An integrated CAPTCHA service is available, however it can be unreliable, and often rejects correct answers.
* Google's reCAPTCHA is available as an option, but requires a little setup.

# reCAPTCHA Setup
* First, ensure your site is accessible from an external domain, as Google will need this.

1) Visit [Register a new site](https://www.google.com/recaptcha/admin/create). Fill in the label, add your domain(s) (just the domain, no subpath, protocol or port), and **Choose the "Challenge (v2) / I'm not a robot Checkbox"** reCAPTCHA type.

![register](/recaptcha/register.png)

2) Click submit. On the next page, copy both the **Site Key** and **Secret Key** and keep them for later.

![keys](/recaptcha/keys.png)

3) Go to jfa-go Settings > Captcha, and enable reCAPTCHA. Paste in the **site key** and **secret key** from above, and fill in the **hostname** to match the one you gave Google.

![settings](/recaptcha/settings.png)


4) Save & restart jfa-go, and you should be good to go. 
