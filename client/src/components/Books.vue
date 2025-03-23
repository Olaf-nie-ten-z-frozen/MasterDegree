<template>
    <div class="container">
      <div class="row">
        <div class="col-sm-10">
          <h1>Books</h1>
          <hr><br><br>
          <alert :message="message" v-if="showMessage"></alert>
          <button type="button" class="btn btn-success btn-sm" @click="openModal('add')">Add Book</button>
          <br><br>
          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">Title</th>
                <th scope="col">Author</th>
                <th scope="col">Read?</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(book, index) in books" :key="index">
                <td>{{ book.title }}</td>
                <td>{{ book.author }}</td>
                <td>
                  <span v-if="book.read">Yes</span>
                  <span v-else>No</span>
                </td>
                <td>
                  <div class="btn-group" role="group">
                    <button type="button" class="btn btn-warning btn-sm" @click="toggleEditBookModal(book)">Update</button>
                    <button type="button" class="btn btn-danger btn-sm" @click="handleDeleteBook(book)">Delete</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
  
      <!-- edit book modal -->
<div
  ref="editBookModal"
  class="modal fade"
  :class="{ show: activeEditBookModal, 'd-block': activeEditBookModal }"
  tabindex="-1"
  role="dialog">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Update</h5>
        <button
          type="button"
          class="close"
          data-dismiss="modal"
          aria-label="Close"
          @click="toggleEditBookModal">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <form>
          <div class="mb-3">
            <label for="editBookTitle" class="form-label">Title:</label>
            <input
              type="text"
              class="form-control"
              id="editBookTitle"
              v-model="editBookForm.title"
              placeholder="Enter title">
          </div>
          <div class="mb-3">
            <label for="editBookAuthor" class="form-label">Author:</label>
            <input
              type="text"
              class="form-control"
              id="editBookAuthor"
              v-model="editBookForm.author"
              placeholder="Enter author">
          </div>
          <div class="mb-3 form-check">
            <input
              type="checkbox"
              class="form-check-input"
              id="editBookRead"
              v-model="editBookForm.read">
            <label class="form-check-label" for="editBookRead">Read?</label>
          </div>
          <div class="btn-group" role="group">
            <button
              type="button"
              class="btn btn-primary btn-sm"
              @click="handleEditSubmit">
              Submit
            </button>
            <button
              type="button"
              class="btn btn-danger btn-sm"
              @click="handleEditCancel">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>
<div v-if="activeEditBookModal" class="modal-backdrop fade show"></div>

<!-- add new book modal -->
    <div
    ref="addBookModal"
    class="modal fade"
    :class="{ show: activeAddBookModal, 'd-block': activeAddBookModal }"
    tabindex="-1"
    role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title">Add a new book</h5>
            <button
            type="button"
            class="close"
            data-dismiss="modal"
            aria-label="Close"
            @click="toggleAddBookModal">
            <span aria-hidden="true">&times;</span>
            </button>
        </div>
        <div class="modal-body">
            <form>
            <div class="mb-3">
                <label for="addBookTitle" class="form-label">Title:</label>
                <input
                type="text"
                class="form-control"
                id="addBookTitle"
                v-model="addBookForm.title"
                placeholder="Enter title">
            </div>
            <div class="mb-3">
                <label for="addBookAuthor" class="form-label">Author:</label>
                <input
                type="text"
                class="form-control"
                id="addBookAuthor"
                v-model="addBookForm.author"
                placeholder="Enter author">
            </div>
            <div class="mb-3 form-check">
                <input
                type="checkbox"
                class="form-check-input"
                id="addBookRead"
                v-model="addBookForm.read">
                <label class="form-check-label" for="addBookRead">Read?</label>
            </div>
            <div class="btn-group" role="group">
                <button
                type="button"
                class="btn btn-primary btn-sm"
                @click="handleAddSubmit">
                Submit
                </button>
                <button
                type="button"
                class="btn btn-danger btn-sm"
                @click="handleAddReset">
                Reset
                </button>
            </div>
            </form>
        </div>
        </div>
    </div>
    </div>
    <div v-if="activeAddBookModal" class="modal-backdrop fade show"></div>
  
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  import Alert from './Alert.vue';
  
  export default {
    data() {
    return {
        activeBookModal: false,
        modalMode: 'add',
        bookForm: { title: '', author: '', read: false },
        addBookForm: { title: '', author: '', read: false },
        editBookForm: { id: '', title: '', author: '', read: false },
        activeEditBookModal: false,
        activeAddBookModal: false,
        books: [],
        message: "",
        showMessage: false,
        editingBookId: null
        
    };
    },
    components: {
      alert: Alert,
    },
    methods: {
        getBooks() {
            axios.get('http://localhost:5000/books')
                .then(res => { this.books = res.data.books; })
                .catch(error => { console.error(error); });
        },
        openModal(mode, book = null) {
            this.modalMode = mode;

            if (mode === 'edit' && book) {
                this.editingBookId = book.id;
                this.bookForm = { ...book };
                this.toggleEditBookModal(book);
            } else {
                this.bookForm = { title: '', author: '', read: false };
                this.toggleAddBookModal();
            }
            },
        editBookForm: {
            id: '', title: '', author: '', read: [],
        },
        initForm() {
            this.addBookForm.title = '';
            this.addBookForm.author = '';
            this.addBookForm = [];
            this.editBookForm.id = '';
            this.editBookForm.author = '';
            this.editBookForm.read = [];
    },
    toggleBookModal() {
        const body = document.querySelector('body');
        this.activeBookModal = !this.activeBookModal;
        body.classList.toggle('modal-open', this.activeBookModal);
        },
    toggleEditBookModal(book) {
        console.log('Opening edit modal for:', book);    
        if (book) {
            this.editBookForm = { ...book }; // tworzymy kopię!
        }
        const body = document.querySelector('body');
        this.activeEditBookModal = !this.activeEditBookModal;
        if (this.activeEditBookModal) {
            body.classList.add('modal-open');
        } else {
            body.classList.remove('modal-open');
        }
        },
        toggleAddBookModal() {
        const body = document.querySelector('body');
        this.activeAddBookModal = !this.activeAddBookModal;
        if (this.activeAddBookModal) {
            body.classList.add('modal-open');
        } else {
            body.classList.remove('modal-open');
        }
        },

      handleSubmit() {
        if (this.modalMode === 'edit') {
          this.handleEditSubmit();
        } else {
          this.handleAddSubmit();
        }
        },
      handleSecondaryAction() {
        if (this.modalMode === 'edit') {
          this.handleEditCancel();
        } else {
          this.handleAddReset();
        }
      },
      handleAddSubmit() {
        axios.post('http://localhost:5000/books', this.addBookForm)
          .then(() => {
            this.getBooks();
            this.message = "Book has been added successfully";
            this.showMessage = true;
            this.toggleBookModal();
          })
          .catch(error => console.log(error));
        },
        updateBook(payload, bookID) {
            axios.put(`http://localhost:5000/books/${bookID}`, payload)
                .then(() => {
                    this.getBooks();
                    this.message = 'Book updated!';
                    this.showMessage = true;
                })
                .catch((error) => {
                    console.error(error);
                    this.getBooks();
            })
      },
      handleEditSubmit() {
        const read = !!this.editBookForm.read;
        const payload = {
            title: this.editBookForm.title,
            author: this.editBookForm.author,
            read,
        };
        axios.put(`http://localhost:5000/books/${this.editBookForm.id}`, payload)
            .then(() => {
            this.getBooks();
            this.message = "Book has been updated successfully";
            this.showMessage = true;
            this.toggleEditBookModal(null);
            })
            .catch(error => console.log(error));
        },

      handleEditCancel() {
        this.toggleBookModal();
        },
        handleEditCancel() { 
            this.toggleEditBookModal(null);
            this.initForm();
            this.getBooks();
        },
      handleAddReset() {
        this.bookForm = { title: '', author: '', read: false };
      },
        handleDeleteBook(book) {
            this.removeBook(book.id);
        },
        removeBook(bookID) {
            axios.delete(`http://localhost:5000/books/${bookID}`)
                .then(() => {
                    this.getBooks();
                    this.message = "Book has been removed.";
                    this.showMessage = true;
                })
                .catch((error) => {
                    console.error(error);
                    this.getBooks;
                });
      },    
    },
    created() {
      this.getBooks();
    },
  };
  </script>
  