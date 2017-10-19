// Scripts for the Coin Counter app

/**
 * Checks the profit field in the UI and colors the card red or green 
 * for the given wallet
 * 
 * @param {string} currency The cryptocurrency for this wallet
 */
function colorCodePanel(currency) {
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
    colorCodePanel("btc");
    colorCodePanel("eth");
    colorCodePanel("ltc");

    $(".trans-profit").each(function(i) {
        console.log($(this).text());
        if (parseFloat($(this).text()) < 0) {
            $(this).text("-$" + Math.abs($(this).text()));
        } else {
            $(this).text("$" + $(this).text());
        }
    });
});