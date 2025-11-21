# 🏔️ Karsog Connect | Business Directory & Marketplace

**Karsog Connect** is a serverless, lightweight local business directory and affiliate marketplace built for the Karsog Valley. It features a modern, responsive frontend connected to a **Google Sheets backend** via Google Apps Script, allowing for real-time updates without a traditional database or server.

-----

## 🚀 Features

  * **Dynamic Directory:** Real-time business listings fetched from Google Sheets.
  * **Smart Search & Filtering:** Instant search by name/category and one-click category filters (Hotels, Taxis, Food, etc.).
  * **Dark/Light Mode:** User-preference based theming with a toggle switch.
  * **WhatsApp Integration:** Direct "Chat" buttons for businesses and "Submit Listing" requests via WhatsApp.
  * **Affiliate Store:** A section to showcase travel essentials or local products with external buy links.
  * **Responsive Design:** optimized for mobile and desktop.
  * **Google Sheets CMS:** Manage all data (businesses, products, featured status) directly from a spreadsheet.

-----

## 🛠️ Tech Stack

  * **Frontend:** HTML5, CSS3 (Custom Properties/Variables), Vanilla JavaScript.
  * **Backend (API):** Google Apps Script.
  * **Database:** Google Sheets.
  * **Icons:** FontAwesome 6.4.0.
  * **Fonts:** Inter & Outfit (Google Fonts).

-----

## ⚙️ Setup & Installation

Follow these steps to deploy your own version of Karsog Connect.

### 1\. Google Sheet Setup (The Database)

1.  Create a new **Google Sheet**.

2.  Rename the first tab to **`Directory`**.

3.  Create a second tab named **`Store`**.

4.  **Add the following Headers (Row 1) exactly:**

    **Directory Sheet:**
    | A | B | C | D | E | F | G | H |
    |---|---|---|---|---|---|---|---|
    | Name | Category | Phone | Desc | Image (URL) | Rating (4.5) | IsFeatured (TRUE/FALSE) | Whatsapp (Phone w/ country code) |

    **Store Sheet:**
    | A | B | C | D | E |
    |---|---|---|---|---|
    | Title | Price | Image (URL) | Link (Amazon/Ext) | Badge (e.g. Sale) |

### 2\. Google Apps Script (The API)

1.  In your Google Sheet, go to **Extensions** \> **Apps Script**.
2.  Delete any code there and paste the following:

<!-- end list -->

```javascript
function doGet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  
  // 1. Fetch Directory
  var dirSheet = ss.getSheetByName("Directory");
  var dirData = [];
  if (dirSheet) {
    var rows = dirSheet.getDataRange().getValues();
    // Start at i=1 to skip headers
    for (var i = 1; i < rows.length; i++) {
      if(rows[i][0] === "") continue; 
      dirData.push({
        name: rows[i][0],
        category: rows[i][1],
        phone: rows[i][2],
        desc: rows[i][3],
        image: rows[i][4],
        rating: rows[i][5],
        isFeatured: rows[i][6],
        whatsapp: rows[i][7]
      });
    }
  }

  // 2. Fetch Store
  var shopSheet = ss.getSheetByName("Store");
  var shopData = [];
  if (shopSheet) {
    var rows = shopSheet.getDataRange().getValues();
    for (var i = 1; i < rows.length; i++) {
      if(rows[i][0] === "") continue;
      shopData.push({
        title: rows[i][0],
        price: rows[i][1],
        image: rows[i][2],
        link: rows[i][3],
        badge: rows[i][4]
      });
    }
  }

  var result = {
    directory: dirData,
    store: shopData
  };

  return ContentService.createTextOutput(JSON.stringify(result))
    .setMimeType(ContentService.MimeType.JSON);
}
```

3.  Click **Save** (Floppy disk icon).
4.  Click **Deploy** \> **New deployment**.
5.  Select type: **Web app**.
6.  **Configuration (Crucial):**
      * **Description:** v1
      * **Execute as:** Me (your email).
      * **Who has access:** **Anyone** (This is required for the frontend to fetch data).
7.  Click **Deploy**.
8.  **Copy the "Web App URL"**.

### 3\. Frontend Configuration

1.  Open the `index.html` file.
2.  Scroll down to the `<script>` section.
3.  Replace the `SHEET_API_URL` variable with your copied Web App URL:

<!-- end list -->

```javascript
const SHEET_API_URL = "https://script.google.com/macros/s/OYour_Copied_URL_Here.../exec";
```

4.  Open `index.html` in your browser. The data from your sheet should now load\!

-----

## 🎨 Customization

### Changing Colors

You can easily change the color scheme by editing the `:root` variables in the CSS section of `index.html`:

```css
:root {
    --primary: #3b82f6;       /* Main Brand Color */
    --accent: #f59e0b;        /* Highlights/Featured Color */
    --bg-body: #0f172a;       /* Dark Mode Background */
    /* ... */
}
```

### Adding Business Categories

1.  In the HTML, find `<div class="categories-grid">`.
2.  Add a new link element.
3.  Update the filter logic in the `setCategory()` and `filterListings()` JavaScript functions to match your new category name.

-----

## 📂 Project Structure

```
/
├── index.html          # The complete frontend (HTML/CSS/JS)
├── README.md           # Project documentation
└── assets/             # (Optional) Local images if not using external URLs
```

-----

## 🤝 Contributing

1.  Fork the repository.
2.  Create a new feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

-----

## 👤 Author

**Aman Choudhary**

  * Location: Karsog, Mandi
  * Role: Developer & Maintainer

-----

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.