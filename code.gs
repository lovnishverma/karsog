function doGet() {
    var ss = SpreadsheetApp.getActiveSpreadsheet();

    // --- 1. Fetch Directory Data ---
    var dirSheet = ss.getSheetByName("Directory");
    var dirData = [];
    if (dirSheet) {
        var rows = dirSheet.getDataRange().getValues();
        // Start loop at i=1 to skip the header row
        for (var i = 1; i < rows.length; i++) {
            if (rows[i][0] === "") continue; // Skip empty rows

            // Collect up to 5 images from columns I, J, K, L, M (Indices 8-12)
            var images = [];
            if (rows[i][8]) images.push(rows[i][8]);
            if (rows[i][9]) images.push(rows[i][9]);
            if (rows[i][10]) images.push(rows[i][10]);
            if (rows[i][11]) images.push(rows[i][11]);
            if (rows[i][12]) images.push(rows[i][12]);

            dirData.push({
                name: rows[i][0],       // Col A
                category: rows[i][1],   // Col B
                phone: rows[i][2],      // Col C
                desc: rows[i][3],       // Col D
                address: rows[i][4],    // Col E (New Address Field)
                rating: rows[i][5],     // Col F
                isFeatured: rows[i][6], // Col G
                whatsapp: rows[i][7],   // Col H
                images: images          // Col I-M (Array of images)
            });
        }
    }

    // --- 2. Fetch Store Data ---
    var shopSheet = ss.getSheetByName("Store");
    var shopData = [];
    if (shopSheet) {
        var rows = shopSheet.getDataRange().getValues();
        for (var i = 1; i < rows.length; i++) {
            if (rows[i][0] === "") continue;
            shopData.push({
                title: rows[i][0],
                price: rows[i][1],
                image: rows[i][2],
                link: rows[i][3],
                badge: rows[i][4]
            });
        }
    }

    // Return JSON
    var result = {
        directory: dirData,
        store: shopData
    };

    return ContentService.createTextOutput(JSON.stringify(result))
        .setMimeType(ContentService.MimeType.JSON);
}