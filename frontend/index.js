const ulEl = document.getElementById("ul-el")
const inputBtn = document.getElementById("input-btn")
const inputBox = document.getElementById("input-box")
const clearBtn = document.getElementById("clear-btn")
const findRecipeBtn = document.getElementById("find-recipe-btn")
const recTbl = document.getElementById("rec-tbl")


let ingredients = []
let filteredData = []
let currentPage = 1
let recipesPerPage = 10

inputBtn.addEventListener("click", function() {
     let value = inputBox.value
     if(value && !ingredients.includes(value))
     {
     ingredients.push(value)
     }
     renderList()
     inputBox.value=""
})

function removeIngredient(index) {
    ingredients.splice(index, 1);
    renderList();
}

function renderList() {
    ulEl.innerHTML = ""
    for(let i=0; i<ingredients.length; i++)
    {
        ulEl.innerHTML +=
        `<li>
        <span>${ingredients[i]}</span> 
        <span style="color: red; cursor: pointer; margin-left: 10px;" onclick="removeIngredient(${i})">
        Delete
        </span>
        </li>`

    }
}

clearBtn.addEventListener("click", function() {
    ulEl.innerHTML = ""
    ingredients = []
    recTbl.innerHTML = ""
})

findRecipeBtn.addEventListener("click", async function() {
    const response = await fetch("http://127.0.0.1:8000/recipes", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ingredients: ingredients})
    });

    let data = await response.json()


    console.log("Received data:", data);

    const checkedboxes_mood = document.querySelectorAll('input[name="mood"]:checked')
    const checkedboxes_category = document.querySelectorAll('input[name="category"]:checked')

    const values_mood = Array.from(checkedboxes_mood).map(cb => cb.value)
    const values_category = Array.from(checkedboxes_category).map(cb => cb.value)

    let checkedvalues = values_mood.concat(values_category)

    checkedvalues = checkedvalues.map(tag => tag.toLowerCase())

    recTbl.innerHTML = ""
    
    if(checkedvalues.length===0)
   {
    data.sort((a,b)=>b.match_count-a.match_count)
   }

   else {
      data.forEach(recipe => {
        const tagMatches = recipe.tags.filter(tag => checkedvalues.includes(tag))
        recipe.tag_match_count = tagMatches.length;
      })

      data.sort((a, b) => {
        if (b.match_count!==a.match_count) {
            return b.match_count - a.match_count
        }

        return b.tag_match_count - a.tag_match_count
      })
       data = data.filter(r => r.tag_match_count>0)
   }

   filteredData = data

   renderRecipes(filteredData, currentPage)

   
});

function renderRecipes(filteredData, currentPage) {
    const startIndex = (currentPage-1)*recipesPerPage
    const endIndex = startIndex + recipesPerPage
    const pageData = filteredData.slice(startIndex, endIndex)

    recTbl.innerHTML="<tr><th>Dish</th> <th>Ingredients</th> <th>Instructions</th></tr>"

    pageData.forEach((recipe, index) => {
        const instructionsId = `instructions-${index}`
        let formattedIngredients = recipe.ingredients.map(ing => `${ing.quantity || ''} ${ing.unit || ''} ${ing.name || ''}`.trim()).join(', <br>')
        
        recTbl.innerHTML += `<tr><td>${recipe.name}<br><img src="${recipe.image}" alt="Image" style="width: 25vw; height: auto; max-height: 200px; object-fit: contain;"></td> <td>${formattedIngredients}</td>
         <td>
         <a href="#" onclick="document.getElementById('${instructionsId}').classList.toggle('hidden'); return false;">
         Recipe
         </a>
         <div id="${instructionsId}" class="hidden" style="margin-top: 10px;">
         ${recipe.instructions.join('<br><br>')}
         </div>
         </td></tr>`
    
    
       });

       renderPaginationControls(filteredData.length)

}

function renderPaginationControls(totalRecipes) {
    const paginationDiv = document.getElementById("pagination-controls");
    paginationDiv.innerHTML = "";
    const totalPages = Math.ceil(totalRecipes / recipesPerPage);


    if(currentPage>1)
    {
        const Backbtn = document.createElement("button");
        Backbtn.textContent = "<"
        Backbtn.onclick = () => {
            currentPage--
            renderRecipes(filteredData, currentPage)
        }
        Backbtn.className = "pagination-btn"
        paginationDiv.appendChild(Backbtn)
    }

    const pageInfo = document.createElement("span");
    pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    pageInfo.style.margin = "0 12px";
    pageInfo.style.fontWeight = "bold";
    paginationDiv.appendChild(pageInfo);



    if(currentPage*recipesPerPage < totalRecipes)
    {
        const Frwdbtn = document.createElement("button");
        Frwdbtn.textContent = ">"
        Frwdbtn.onclick = () => {
            currentPage++
            renderRecipes(filteredData, currentPage)
        }
        Frwdbtn.className = "pagination-btn"

        paginationDiv.appendChild(Frwdbtn)
    }
}
