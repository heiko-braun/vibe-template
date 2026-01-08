/**
 * Centralized API configuration composable
 * Returns the base URL for API calls based on environment
 */
export const useApi = () => {
  const config = useRuntimeConfig()
  const apiBaseUrl = config.public.apiBaseUrl as string

  async function fetchItems() {
    const response = await fetch(`${apiBaseUrl}/api/items/`)
    if (!response.ok) {
      throw new Error('Failed to fetch items')
    }
    return response.json()
  }

  async function createItem(data: { title: string; description?: string }) {
    const response = await fetch(`${apiBaseUrl}/api/items/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    if (!response.ok) {
      throw new Error('Failed to create item')
    }
    return response.json()
  }

  async function updateItem(id: number, data: { title: string; description?: string }) {
    const response = await fetch(`${apiBaseUrl}/api/items/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    if (!response.ok) {
      throw new Error('Failed to update item')
    }
    return response.json()
  }

  async function deleteItem(id: number) {
    const response = await fetch(`${apiBaseUrl}/api/items/${id}`, {
      method: 'DELETE',
    })
    if (!response.ok) {
      throw new Error('Failed to delete item')
    }
  }

  return {
    fetchItems,
    createItem,
    updateItem,
    deleteItem,
  }
}
