class BooksDB {
    saveIntoDB(favorite) {
        const favorites = this.getFromDB();
        favorites.push(favorite);
        localStorage.setItem('favorites', JSON.stringify(favorites));
    }

    getFromDB() {
        let favorites = [];
        const storedFavorites = localStorage.getItem('favorites');
        if (storedFavorites) {
            favorites = JSON.parse(storedFavorites);
        }
        return favorites;
    }

    removeFromDB(id) {
        let favorites = this.getFromDB();
        favorites = favorites.filter(favorite => favorite.id !== id);
        localStorage.setItem('favorites', JSON.stringify(favorites));
    }
}

const mybooksDB = new BooksDB();

document.addEventListener('click', function(book) {
    favoriteBook(book);
});

function favoriteBook(book) {
    if (book.target.classList.contains('favHeart')) {
        if (book.target.classList.contains('isFavorite')) {
            book.target.classList.remove('isFavorite');
            book.target.classList.remove('fa-solid');
            mybooksDB.removeFromDB(book.target.dataset.id);
        } else {
            book.target.classList.add('isFavorite');
            book.target.classList.add('fa-solid');
            const bookBody = book.target.parentElement.parentElement;
            const bookInfo = {
                id: book.target.dataset.id,
                name: bookBody.querySelector('.book-title').textContent.trim(),
                image: bookBody.querySelector('.book-image').src
            };
            mybooksDB.saveIntoDB(bookInfo);
        }
    }
}

class UI {
    displayFavoritesTable(favorites) {
        const favoritesTable = document.querySelector('#favorites-table tbody');
        // Check if favoritesTable exists
        if (!favoritesTable) {
            console.error("Favorites table tbody not found.");
            return;
        }
        favorites.forEach(favorite => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>
                    <img src="${favorite.image}" alt="${favorite.name}">
                </td>
                <td>
                    <a href="book_detail/${favorite.id}">${favorite.name}</a>
                </td>
                <td>
                    <button class="btn btn-danger remove-favorite" data-id="${favorite.id}">-</button>
                </td>
            `;
            favoritesTable.appendChild(tr);
        });
        // Mark favorites after displaying them
        this.isFavorite();
    }

    removeFavorite(element) {
        element.remove();
    }

    isFavorite() {
        const favorites = mybooksDB.getFromDB();
        favorites.forEach(favorite => {
            const favoriteBook = document.querySelector(`[data-id="${favorite.id}"]`);
            if (favoriteBook) {
                favoriteBook.classList.add('isFavorite');
                favoriteBook.classList.add('fa-solid');
            }
        });
    }
}

const ui = new UI();

function documentReady() {
    // Display
    ui.isFavorite();

    const favoritesTable = document.querySelector('#favorites-table tbody');
    if (favoritesTable) {
        const favorites = mybooksDB.getFromDB();
        ui.displayFavoritesTable(favorites);
        favoritesTable.addEventListener('click', (e) => {
            e.preventDefault();
            if (e.target.classList.contains('remove-favorite')) {
                ui.removeFavorite(e.target.parentElement.parentElement);
                mybooksDB.removeFromDB(e.target.dataset.id);
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", documentReady);
