// Scripts for the Coin Counter app

/**
 * Checks the profit field in the UI and colors the card red or green 
 * for the given wallet
 * 
 * @param {string} currency The cryptocurrency for this wallet
 */
function colorCode(currency) {
    var profitID = "#" + currency + "--profit";
    var cardID = "#" + currency + "--card";
    if (parseFloat($(profitID).text()) < 0) {
        $(cardID + " > .card-header").addClass("deep-orange");
        $(cardID + " > .card-footer").addClass("deep-orange");
    } else {
        $(cardID + " > .card-header").addClass("light-green");
        $(cardID + " > .card-footer").addClass("light-green");
    }
}

$(function() {
    colorCode("btc");
    colorCode("eth");
    colorCode("ltc");
});