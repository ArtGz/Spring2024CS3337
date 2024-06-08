function loadSearch() {
    let search = document.getElementById("search-bar")
    let menu = document.getElementById("search-menu")
    let results = document.getElementsByClassName("search-result");
    let noResults = document.getElementById("blank-result");

    if(!search){
        return;
    }

    search.addEventListener("focus", function(){
        menu.classList.add("show");
    });

    search.addEventListener("focusout", function(event){
        let element = event.relatedTarget

        // Don't close on search result click / Make sure to close on hamburger click
        if(!element || element && !["dropdown-item", "search"].every(name => element.classList.contains(name))){
            menu.classList.remove("show");
        }
    });

    search.addEventListener("input", function(){
        if(search.value.trim() === ""){
            for(let x = 0; x < results.length; x++){
                results[x].setAttribute("hidden","");
            }
            return;
        }

        fetch("http://localhost:8000/api/books/" + search.value)
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`API returned error ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                noResults.hidden = data.length == 0 ? null : "hidden";

                let i = 0
                data.forEach((element)=>{
                    if(i < results.length){
                        results[i].querySelector('img').src = "http://localhost:8000/static/" + element[0].substring(14);
                        results[i].querySelector('a').href = "http://localhost:8000/book_detail/" + element[2];
                        results[i].querySelector('span').textContent = element[1];
                        results[i].hidden = null;
                    }
                    i++;
                })

                for(let x = data.length; x < results.length; x++){
                    results[x].setAttribute("hidden","");
                }
            })
            .catch((error) => {
                console.log("Logic error occured in search:");
                console.log(error);
            });
    });
};

window.onload = loadSearch;

