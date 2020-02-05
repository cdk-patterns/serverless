exports.handler = async function(flavour:any) {
    console.log("Requested Pizza :", JSON.stringify(flavour, undefined, 2));
    
    let containsPineapple = false;
    
    if(flavour == 'pineapple' || flavour =='hawaiian'){
        containsPineapple = true;
    }

    return {'containsPineapple': containsPineapple}
}