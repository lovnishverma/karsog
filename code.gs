// ==========================================
// 1. READ DATA (Frontend fetches this)
// ==========================================
function doGet(e) {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var action = e.parameter.action;
    
    // A. Get Stats
    if (action === 'getStats') {
        var bizId = e.parameter.bizId;
        var period = parseInt(e.parameter.period) || 7;
        return getBusinessStats(ss, bizId, period);
    }
    
    // B. Get Directory Data
    var dirSheet = ss.getSheetByName("Directory");
    var dirData = [];
    
    if (dirSheet) {
        var rows = dirSheet.getDataRange().getValues();
        
        // Start at i=1 to skip Header row
        for (var i = 1; i < rows.length; i++) {
            // If Name (Col B / Index 1) is empty, skip
            if (!rows[i][1]) continue; 

            // COLLECT IMAGES (Cols J, K, L, M, N -> Indices 9, 10, 11, 12, 13)
            var images = [];
            if (rows[i][9])  images.push(String(rows[i][9]));
            if (rows[i][10]) images.push(String(rows[i][10]));
            if (rows[i][11]) images.push(String(rows[i][11]));
            if (rows[i][12]) images.push(String(rows[i][12]));
            if (rows[i][13]) images.push(String(rows[i][13]));

            dirData.push({
                timestamp:  rows[i][0],  // Col A
                name:       rows[i][1],  // Col B
                category:   rows[i][2],  // Col C
                phone:      rows[i][3],  // Col D
                desc:       rows[i][4],  // Col E
                address:    rows[i][5],  // Col F
                rating:     rows[i][6],  // Col G
                isFeatured: rows[i][7],  // Col H
                whatsapp:   rows[i][8],  // Col I
                images:     images,      // Cols J-N
                id:         rows[i][14]  // Col O (ID)
            });
        }
    }

    // C. Get Store Data
    var shopSheet = ss.getSheetByName("Store");
    var shopData = [];
    if (shopSheet) {
        var rows = shopSheet.getDataRange().getValues();
        for (var i = 1; i < rows.length; i++) {
            if (!rows[i][0]) continue;
            shopData.push({
                title: rows[i][0], price: rows[i][1], image: rows[i][2],
                link:  rows[i][3], badge: rows[i][4]
            });
        }
    }

    return ContentService.createTextOutput(JSON.stringify({
        directory: dirData,
        store: shopData
    })).setMimeType(ContentService.MimeType.JSON);
}

// ==========================================
// 2. WRITE ANALYTICS
// ==========================================
function doPost(e) {
    try {
        var ss = SpreadsheetApp.getActiveSpreadsheet();
        var sheet = ss.getSheetByName("stats");
        if (!sheet) {
            sheet = ss.insertSheet("stats");
            sheet.appendRow(["Timestamp", "Business ID", "Action Type", "Value"]);
        }
        var data = JSON.parse(e.postData.contents);
        sheet.appendRow([ new Date(), data.id, data.type, data.value ]);
        return ContentService.createTextOutput("OK").setMimeType(ContentService.MimeType.TEXT);
    } catch (error) {
        return ContentService.createTextOutput("Error: " + error.toString());
    }
}

// ==========================================
// 3. AUTOMATION: Form -> Directory Sheet
// ==========================================
function onFormSubmit(e) {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var dirSheet = ss.getSheetByName("Directory");
    if (!dirSheet) return;

    var v = e.values; // Short for values

    // MAPPING BASED ON YOUR FORM QUESTIONS:
    // 0:Timestamp, 1:Name, 2:Cat, 3:Phone, 4:Desc, 5:Addr, 6:Rating, 7:Featured, 8:WA
    // 9:Img1, 10:Img2, 11:Img3, 12:Img4, 13:Img5, 14:ID

    // Check if ID (Index 14) is submitted. If empty, generate one.
    var businessId = v[14];
    if (!businessId || businessId === "") {
        businessId = Utilities.getUuid().slice(0, 8);
    }

    // Prepare Row
    var newRow = [
        v[0], // Timestamp
        v[1], // Name
        v[2], // Category
        v[3], // Phone
        v[4], // Desc
        v[5], // Address
        v[6], // Rating
        v[7], // isFeatured
        v[8], // Whatsapp
        v[9], // Image 1
        v[10], // Image 2
        v[11], // Image 3
        v[12], // Image 4
        v[13], // Image 5
        businessId // ID
    ];

    dirSheet.appendRow(newRow);
}

// ==========================================
// 4. HELPER: Stats
// ==========================================
function getBusinessStats(ss, bizId, period) {
    var statsSheet = ss.getSheetByName("stats");
    if (!statsSheet) return ContentService.createTextOutput(JSON.stringify({ views: 0 })).setMimeType(ContentService.MimeType.JSON);
    
    var data = statsSheet.getDataRange().getValues();
    var cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - period);
    var stats = { views: 0, phone: 0, whatsapp: 0, recentActivity: [], dailyData: {} };
    
    for (var i = 1; i < data.length; i++) {
        var timestamp = new Date(data[i][0]);
        var recordBizId = String(data[i][1]);
        var actionType = String(data[i][2]);
        
        if (recordBizId !== bizId || timestamp < cutoffDate) continue;
        
        if (actionType === "view") stats.views++;
        if (actionType === "phone") stats.phone++;
        if (actionType === "whatsapp") stats.whatsapp++;
        
        var dateKey = Utilities.formatDate(timestamp, Session.getScriptTimeZone(), "yyyy-MM-dd");
        if (!stats.dailyData[dateKey]) stats.dailyData[dateKey] = { views: 0, phone: 0, whatsapp: 0 };
        stats.dailyData[dateKey][actionType]++;
        
        stats.recentActivity.push({ type: actionType, timestamp: timestamp.toISOString() });
    }
    
    stats.recentActivity.sort(function(a, b) { return new Date(b.timestamp) - new Date(a.timestamp); });
    stats.recentActivity = stats.recentActivity.slice(0, 20);
    
    return ContentService.createTextOutput(JSON.stringify(stats)).setMimeType(ContentService.MimeType.JSON);
}