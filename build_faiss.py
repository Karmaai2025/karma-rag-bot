from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader

# Load your PDF and split into chunks
loader = PyPDFLoader("karma_content.pdf")
docs = loader.load_and_split()

# Create embeddings
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key="AIzaSyDwv_96yoBnczeNSWLbHSBCTPQ6gbkMVLM"
)

# Build FAISS index
vectorstore = FAISS.from_documents(docs, embedding)

# Save index to disk
vectorstore.save_local("karma_index")
print("FAISS index created and saved to karma_index/")