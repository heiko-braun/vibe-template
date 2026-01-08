<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          App Template
        </h1>
        <p class="text-lg text-gray-600 dark:text-gray-400">
          Fullstack web application template with FastAPI & Nuxt 3
        </p>
      </div>

      <!-- Items List -->
      <div class="mb-8">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-semibold text-gray-900 dark:text-white">Items</h2>
          <UButton @click="showCreateModal = true" color="primary">
            Add Item
          </UButton>
        </div>

        <div v-if="loading" class="text-center py-8">
          <p class="text-gray-600 dark:text-gray-400">Loading...</p>
        </div>

        <div v-else-if="error" class="text-center py-8">
          <p class="text-red-600">{{ error }}</p>
        </div>

        <div v-else-if="items.length === 0" class="text-center py-8">
          <p class="text-gray-600 dark:text-gray-400">No items yet. Create one to get started!</p>
        </div>

        <div v-else class="grid gap-4">
          <UCard v-for="item in items" :key="item.id" class="hover:shadow-lg transition-shadow">
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                  {{ item.title }}
                </h3>
                <p class="text-gray-600 dark:text-gray-400 mb-4">
                  {{ item.description || 'No description' }}
                </p>
                <p class="text-sm text-gray-500">
                  Created: {{ new Date(item.created_at).toLocaleString() }}
                </p>
              </div>
              <div class="flex gap-2 ml-4">
                <UButton @click="editItem(item)" color="gray" size="sm">Edit</UButton>
                <UButton @click="deleteItemConfirm(item.id)" color="red" size="sm">Delete</UButton>
              </div>
            </div>
          </UCard>
        </div>
      </div>

      <!-- Create/Edit Modal -->
      <UModal v-model="showCreateModal">
        <UCard>
          <template #header>
            <h3 class="text-lg font-semibold">{{ editingItem ? 'Edit Item' : 'Create Item' }}</h3>
          </template>

          <div class="space-y-4">
            <UFormGroup label="Title" required>
              <UInput v-model="formData.title" placeholder="Enter title" />
            </UFormGroup>

            <UFormGroup label="Description">
              <UTextarea v-model="formData.description" placeholder="Enter description" />
            </UFormGroup>
          </div>

          <template #footer>
            <div class="flex justify-end gap-2">
              <UButton @click="showCreateModal = false" color="gray">Cancel</UButton>
              <UButton @click="submitForm" color="primary">
                {{ editingItem ? 'Update' : 'Create' }}
              </UButton>
            </div>
          </template>
        </UCard>
      </UModal>
    </div>
  </div>
</template>

<script setup>
const { fetchItems, createItem, updateItem, deleteItem } = useApi()

const items = ref([])
const loading = ref(true)
const error = ref(null)
const showCreateModal = ref(false)
const editingItem = ref(null)
const formData = ref({
  title: '',
  description: ''
})

// Load items on mount
onMounted(async () => {
  await loadItems()
})

async function loadItems() {
  loading.value = true
  error.value = null
  try {
    items.value = await fetchItems()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function editItem(item) {
  editingItem.value = item
  formData.value = {
    title: item.title,
    description: item.description
  }
  showCreateModal.value = true
}

async function submitForm() {
  try {
    if (editingItem.value) {
      await updateItem(editingItem.value.id, formData.value)
    } else {
      await createItem(formData.value)
    }
    showCreateModal.value = false
    editingItem.value = null
    formData.value = { title: '', description: '' }
    await loadItems()
  } catch (e) {
    error.value = e.message
  }
}

async function deleteItemConfirm(id) {
  if (confirm('Are you sure you want to delete this item?')) {
    try {
      await deleteItem(id)
      await loadItems()
    } catch (e) {
      error.value = e.message
    }
  }
}
</script>
