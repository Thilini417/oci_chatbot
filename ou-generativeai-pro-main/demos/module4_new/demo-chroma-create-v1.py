from langchain_community.embeddings import OCIGenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_chroma import Chroma
from LoadProperties import LoadProperties

#This demo creates Chroma Vector Store

# Step 1 - load and split documents

pdf_loader = PyPDFDirectoryLoader("./pdf-docs" )
loaders = [pdf_loader]

documents = []
for loader in loaders:
    documents.extend(loader.load())

text_splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=100)
all_documents = text_splitter.split_documents(documents)

print(f"Total number of documents: {len(all_documents)}")

#Step 2 - setup OCI Generative AI llm

#properties = LoadProperties()

embeddings = OCIGenAIEmbeddings(
    model_id="cohere.embed-english-v3.0",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id="ocid1.tenancy.oc1..aaaaaaaa77cvvhxu6a7dauvbzrhxeoamifazsqzl47ygggdhbrjymt2zmu2q",
    model_kwargs={"truncate":True}
)

#Step 3 - since OCIGenAIEmbeddings accepts only 96 documents in one run , we will input documents in batches.

# Set the batch size
batch_size = 96

# Calculate the number of batches
num_batches = len(all_documents) // batch_size + (len(all_documents) % batch_size > 0)

db = Chroma(embedding_function=embeddings , persist_directory="./chromadb")
retv = db.as_retriever()

# Iterate over batches
for batch_num in range(num_batches):
    # Calculate start and end indices for the current batch
    start_index = batch_num * batch_size
    end_index = (batch_num + 1) * batch_size
    # Extract documents for the current batch
    batch_documents = all_documents[start_index:end_index]
    # Your code to process each document goes here
    retv.add_documents(batch_documents)
    print(start_index, end_index)

#Step 4 - here we persist the collection
#Since Chroma 0.4.x the manual persistence method is no longer supported as docs are automatically persisted.
#db.persist()





