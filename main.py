from loader.loader import ProjectLoader

loader = ProjectLoader()
vector_store = loader.load("/Users/ishaan915/Me/projects/logo-processor")
print(loader.vector_store.peek())

