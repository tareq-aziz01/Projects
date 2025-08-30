import streamlit as st
import requests

# ----------------- Book Fetcher -----------------
def get_books(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=6"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("items", [])
    return []

# ----------------- Page Config -----------------
st.set_page_config(page_title="📚 Smart Book Recommender", layout="wide")

# ----------------- Session State for Saved Books -----------------
if "saved_books" not in st.session_state:
    st.session_state.saved_books = []

# ----------------- Custom CSS -----------------
st.markdown("""
    <style>
    .stApp { background-color: #0f1117; color: white; }
    .book-card {
        background: #1e1e2f;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
        transition: transform 0.2s;
    }
    .book-card:hover {
        transform: scale(1.03);
        box-shadow: 0px 6px 16px rgba(0,0,0,0.6);
    }
    .book-title {
        font-size: 18px;
        font-weight: bold;
        color: #ffd369;
    }
    .book-author {
        font-size: 14px;
        color: #eeeeee;
    }
    .book-desc {
        font-size: 13px;
        color: #bbbbbb;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- Sidebar Menu -----------------
menu = st.sidebar.radio(
    "📖 Menu",
    ["🔎 Search Books", "🔖 Saved Books", "📷 Scan Book"]
)

# ----------------- Search Books Page -----------------
if menu == "🔎 Search Books":
    st.markdown("<h1 style='text-align: center; color: #ffd369;'>📚 Smart Book Recommender</h1>", unsafe_allow_html=True)
    st.write("🔎 *Enter a topic or keyword and discover amazing books!*")

    query = st.text_input("Enter a topic or keyword:")

    if st.button("Search Books"):
        if query:
            books = get_books(query)
            if books:
                st.subheader("✨ Recommended Books")
                cols = st.columns(3)
                for i, book in enumerate(books):
                    info = book["volumeInfo"]
                    title = info.get("title", "No Title")
                    authors = ", ".join(info.get("authors", ["Unknown Author"]))
                    publisher = info.get("publisher", "Unknown Publisher")
                    published_date = info.get("publishedDate", "Unknown Date")
                    description = info.get("description", "No description available.")[:180] + "..."
                    rating = info.get("averageRating", "N/A")
                    image = info.get("imageLinks", {}).get("thumbnail", "https://via.placeholder.com/128x195.png?text=No+Cover")
                    
                    with cols[i % 3]:
                        st.markdown(f"""
                            <div class="book-card">
                                <img src="{image}" width="120">
                                <div class="book-title">{title}</div>
                                <div class="book-author">👤 {authors}</div>
                                <div class="book-author">🏢 {publisher} ({published_date})</div>
                                <div class="book-author">⭐ Rating: {rating}</div>
                                <div class="book-desc">{description}</div>
                            </div>
                        """, unsafe_allow_html=True)

                        if st.button(f"💾 Save '{title}'", key=f"save_{i}"):
                            st.session_state.saved_books.append({
                                "title": title,
                                "authors": authors,
                                "publisher": publisher,
                                "date": published_date,
                                "rating": rating,
                                "image": image
                            })
                            st.success(f"✅ '{title}' saved!")
            else:
                st.warning("No books found! Try another keyword.")
        else:
            st.error("Please enter a topic before searching.")

# ----------------- Saved Books Page -----------------
elif menu == "🔖 Saved Books":
    st.markdown("<h2 style='color:#ffd369;'>🔖 Your Saved Books</h2>", unsafe_allow_html=True)

    if st.session_state.saved_books:
        cols = st.columns(3)
        for i, book in enumerate(st.session_state.saved_books):
            with cols[i % 3]:
                st.markdown(f"""
                    <div class="book-card">
                        <img src="{book['image']}" width="120">
                        <div class="book-title">{book['title']}</div>
                        <div class="book-author">👤 {book['authors']}</div>
                        <div class="book-author">🏢 {book['publisher']} ({book['date']})</div>
                        <div class="book-author">⭐ Rating: {book['rating']}</div>
                    </div>
                """, unsafe_allow_html=True)

                if st.button(f"🗑 Remove '{book['title']}'", key=f"remove_{i}"):
                    st.session_state.saved_books.pop(i)
                    st.experimental_rerun()
    else:
        st.info("📂 You haven’t saved any books yet!")

# ----------------- Scan Book Page -----------------
elif menu == "📷 Scan Book":
    st.markdown("<h2 style='color:#ffd369;'>📷 Scan a Book</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload a book cover image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="📖 Uploaded Book Cover", use_column_width=True)
        st.success("🚀 Future Feature: AI will detect book details from cover!")
