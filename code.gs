function doGet(e) {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var action = e.parameter.action;
    
    // If requesting stats for a specific business
    if (action === 'getStats') {
        var bizId = e.parameter.bizId;
        var period = parseInt(e.parameter.period) || 7;
        return getBusinessStats(ss, bizId, period);
    }
    
    // Default: Return directory and store data
    var dirSheet = ss.getSheetByName("Directory");
    var dirData = [];
    if (dirSheet) {
        var rows = dirSheet.getDataRange().getValues();
        for (var i = 1; i < rows.length; i++) {
            if (rows[i][0] === "") continue;

            var images = [];
            if (rows[i][8]) images.push(rows[i][8]);
            if (rows[i][9]) images.push(rows[i][9]);
            if (rows[i][10]) images.push(rows[i][10]);
            if (rows[i][11]) images.push(rows[i][11]);
            if (rows[i][12]) images.push(rows[i][12]);

            dirData.push({
                id: rows[i][13],
                name: rows[i][0],
                category: rows[i][1],
                phone: rows[i][2],
                desc: rows[i][3],
                address: rows[i][4],
                rating: rows[i][5],
                isFeatured: rows[i][6],
                whatsapp: rows[i][7],
                images: images
            });
        }
    }

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

    return ContentService.createTextOutput(JSON.stringify({
        directory: dirData,
        store: shopData
    })).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
    try {
        var ss = SpreadsheetApp.getActiveSpreadsheet();
        var sheet = ss.getSheetByName("stats");
        
        if (!sheet) {
            sheet = ss.insertSheet("stats");
            sheet.appendRow(["Timestamp", "Business ID", "Action Type", "Value"]);
        }

        var data = JSON.parse(e.postData.contents);

        sheet.appendRow([
            new Date(),
            data.id,
            data.type,
            data.value
        ]);

        return ContentService.createTextOutput("OK").setMimeType(ContentService.MimeType.TEXT);
    } catch (error) {
        return ContentService.createTextOutput("Error: " + error.toString());
    }
}

// Get stats for a specific business
function getBusinessStats(ss, bizId, period) {
    var statsSheet = ss.getSheetByName("stats");
    
    if (!statsSheet) {
        return ContentService.createTextOutput(JSON.stringify({
            views: 0,
            phone: 0,
            whatsapp: 0,
            recentActivity: [],
            dailyData: {}
        })).setMimeType(ContentService.MimeType.JSON);
    }
    
    var data = statsSheet.getDataRange().getValues();
    var cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - period);
    
    var stats = {
        views: 0,
        phone: 0,
        whatsapp: 0,
        recentActivity: [],
        dailyData: {}
    };
    
    // Process stats
    for (var i = 1; i < data.length; i++) {
        var timestamp = new Date(data[i][0]);
        var recordBizId = String(data[i][1]);
        var actionType = String(data[i][2]);
        
        if (recordBizId !== bizId) continue;
        if (timestamp < cutoffDate) continue;
        
        // Count totals
        if (actionType === "view") stats.views++;
        if (actionType === "phone") stats.phone++;
        if (actionType === "whatsapp") stats.whatsapp++;
        
        // Track daily data
        var dateKey = Utilities.formatDate(timestamp, Session.getScriptTimeZone(), "yyyy-MM-dd");
        if (!stats.dailyData[dateKey]) {
            stats.dailyData[dateKey] = { views: 0, phone: 0, whatsapp: 0 };
        }
        stats.dailyData[dateKey][actionType]++;
        
        // Recent activity (last 20)
        stats.recentActivity.push({
            type: actionType,
            timestamp: timestamp.toISOString()
        });
    }
    
    // Sort recent activity by date (newest first) and limit to 20
    stats.recentActivity.sort(function(a, b) {
        return new Date(b.timestamp) - new Date(a.timestamp);
    });
    stats.recentActivity = stats.recentActivity.slice(0, 20);
    
    return ContentService.createTextOutput(JSON.stringify(stats))
        .setMimeType(ContentService.MimeType.JSON);
}