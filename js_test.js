function sortByPriceAscending(jsonString) {   

    var jsonArray = JSON.parse(jsonString)

    function custonSort(a, b) {
      if(a.price == b.price){ 
        
        if(a.name == b.name) {
            return 0
        }
        
        return  a.name > b.name ? 1 : -1;
      }
      return  a.price > b.price ? 1 : -1;
    }
    jsonArray.sort(custonSort);
    console.log(jsonArray);
    return JSON.stringify(jsonArray)
}
  
console.log(sortByPriceAscending('[{"name":"eggs","price":1},{"name":"coffee","price":9.99},{"name":"rice","price":4.04},{"name":"zice","price":4.04}]'));