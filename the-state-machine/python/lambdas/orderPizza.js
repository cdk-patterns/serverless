"use strict";
exports.handler = async function (flavour) {
    console.log("Requested Pizza :", JSON.stringify(flavour, undefined, 2));
    let containsPineapple = false;
    if (flavour == 'pineapple' || flavour == 'hawaiian') {
        containsPineapple = true;
    }
    return { 'containsPineapple': containsPineapple };
};
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoib3JkZXJQaXp6YS5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIm9yZGVyUGl6emEudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IjtBQUFBLE9BQU8sQ0FBQyxPQUFPLEdBQUcsS0FBSyxXQUFVLE9BQVc7SUFDeEMsT0FBTyxDQUFDLEdBQUcsQ0FBQyxtQkFBbUIsRUFBRSxJQUFJLENBQUMsU0FBUyxDQUFDLE9BQU8sRUFBRSxTQUFTLEVBQUUsQ0FBQyxDQUFDLENBQUMsQ0FBQztJQUV4RSxJQUFJLGlCQUFpQixHQUFHLEtBQUssQ0FBQztJQUU5QixJQUFHLE9BQU8sSUFBSSxXQUFXLElBQUksT0FBTyxJQUFHLFVBQVUsRUFBQztRQUM5QyxpQkFBaUIsR0FBRyxJQUFJLENBQUM7S0FDNUI7SUFFRCxPQUFPLEVBQUMsbUJBQW1CLEVBQUUsaUJBQWlCLEVBQUMsQ0FBQTtBQUNuRCxDQUFDLENBQUEiLCJzb3VyY2VzQ29udGVudCI6WyJleHBvcnRzLmhhbmRsZXIgPSBhc3luYyBmdW5jdGlvbihmbGF2b3VyOmFueSkge1xyXG4gICAgY29uc29sZS5sb2coXCJSZXF1ZXN0ZWQgUGl6emEgOlwiLCBKU09OLnN0cmluZ2lmeShmbGF2b3VyLCB1bmRlZmluZWQsIDIpKTtcclxuICAgIFxyXG4gICAgbGV0IGNvbnRhaW5zUGluZWFwcGxlID0gZmFsc2U7XHJcbiAgICBcclxuICAgIGlmKGZsYXZvdXIgPT0gJ3BpbmVhcHBsZScgfHwgZmxhdm91ciA9PSdoYXdhaWlhbicpe1xyXG4gICAgICAgIGNvbnRhaW5zUGluZWFwcGxlID0gdHJ1ZTtcclxuICAgIH1cclxuXHJcbiAgICByZXR1cm4geydjb250YWluc1BpbmVhcHBsZSc6IGNvbnRhaW5zUGluZWFwcGxlfVxyXG59Il19