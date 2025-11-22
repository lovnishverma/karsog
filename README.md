# Karsog.com - Valley Business Directory & Store

A hyper-local business directory and affiliate store website built with **HTML/CSS/JavaScript** on the frontend and powered by **Google Sheets** as the CMS (Content Management System) via Google Apps Script.


[Google form](https://forms.gle/HrJppPH3BHZLSCPD7)


## 🌟 Features

  * **Dynamic Content:** All listings and products are fetched in real-time from a Google Sheet.
  * **Responsive Design:** Fully optimized for mobile, tablet, and desktop.
  * **Dark/Light Mode:** Built-in theme toggler with persistent preferences.
  * **Search & Filtering:** Client-side search and category filtering (Hotels, Taxis, Food, etc.).
  * **Rich Listings:** detailed business cards with Image Carousels (up to 5 images), WhatsApp integration, and Click-to-Call.
  * **Affiliate Store:** A dedicated section for showcasing products.
  * **Emergency Bar:** Quick access to police and ambulance numbers.
  * **SEO Friendly:** Semantic HTML structure and meta tags.

## 📂 Project Structure

```text
/
├── index.html      # The main frontend code (HTML + Embedded CSS & JS)
├── Code.gs         # Google Apps Script code (The Backend API)
└── README.md       # Documentation
```

## 🚀 Setup Guide

### Step 1: Google Sheets Setup (The Database)

1.  Create a new [Google Sheet](https://sheets.new).
2.  Create two tabs (sheets) named exactly: `Directory` and `Store`.

#### **Sheet 1: "Directory" Columns**

| Column | Header Name (Suggestion) | Data Type | Description |
| :--- | :--- | :--- | :--- |
| **A** | Name | Text | Business Name |
| **B** | Category | Text | Options: `Hotel`, `Taxi`, `Shop`, `Food`, `Service`, `Health` |
| **C** | Phone | Text | Phone number |
| **D** | Description | Text | Short description |
| **E** | Address | Text | Full physical address |
| **F** | Rating | Number | E.g., `4.5` |
| **G** | Featured | Boolean | `TRUE` or `FALSE` (Highlights the card) |
| **H** | WhatsApp | Number | Phone number without `+` (e.g., `919876543210`) |
| **I** | Image 1 | URL | Direct link to image |
| **J** | Image 2 | URL | (Optional) Additional image |
| **K** | Image 3 | URL | (Optional) Additional image |
| **L** | Image 4 | URL | (Optional) Additional image |
| **M** | Image 5 | URL | (Optional) Additional image |

#### **Sheet 2: "Store" Columns**

| Column | Header Name | Description |
| :--- | :--- | :--- |
| **A** | Title | Product Name |
| **B** | Price | Product Price (just the number) |
| **C** | Image URL | Direct link to product image |
| **D** | Buy Link | Affiliate/Purchase URL |
| **E** | Badge | E.g., `Sale`, `New`, `Hot` |

-----

### Step 2: Deploy Google Apps Script (The API)

1.  In your Google Sheet, go to **Extensions \> Apps Script**.
2.  Delete any existing code and paste the contents of the `Code.gs` provided below (or from your snippet).
3.  Click **Save**.
4.  Click the blue **Deploy** button \> **New Deployment**.
5.  **Select type:** Web App.
6.  **Configuration:**
      * **Description:** Karsog API v1
      * **Execute as:** Me
      * **Who has access:** **Anyone** (Crucial for the site to work publicly).
7.  Click **Deploy**.
8.  **Copy the Web App URL** (It ends in `/exec`).

-----

### Step 3: Connect Frontend

1.  Open `index.html`.
2.  Scroll down to the `<script>` section at the bottom.
3.  Replace the `SHEET_API_URL` variable with your Web App URL from Step 2.

<!-- end list -->

```javascript
// Replace this string
const SHEET_API_URL = "https://script.google.com/macros/s/AKfy.../exec";
```

4.  Save the file.

-----

### Step 4: Form Submission Setup

The "Join" form in the HTML uses WhatsApp for submissions by default.

1.  Find the `submitForm` function in `index.html`.
2.  Replace the phone number in the `window.open` line with your admin WhatsApp number.

<!-- end list -->

```javascript
window.open(`https://wa.me/91YOUR_NUMBER_HERE?text=${msg}`, '_blank');
```

## 🛠 Technologies Used

  * **Frontend:** HTML5, CSS3 (Flexbox/Grid), JavaScript (ES6+).
  * **Icons:** FontAwesome 6.4 (CDN).
  * **Fonts:** Google Fonts (Inter, Outfit).
  * **Backend:** Google Apps Script.
  * **Database:** Google Sheets.

## 🎨 Customization

  * **Colors:** Edit the `:root` variables in the `<style>` section of `index.html` to change the color scheme.
    ```css
    :root {
        --primary: #3b82f6; /* Main Brand Color */
        --accent: #f59e0b;  /* Highlight Color */
    }
    ```
  * **Logo:** Locate `.logo` in the HTML and change the text or icon.

## 📢 Deployment

Since this is a static site, you can host it for free on:

1.  **GitHub Pages:** Upload `index.html` to a repository and enable Pages.
2.  **Netlify / Vercel:** Drag and drop the folder containing `index.html`.

## 📄 License

This project is not open-source and free to use.

-----

**Developed for Karsog Valley**