import { defineStore } from 'pinia'

export const useGlobalFilterStore = defineStore('globalFilter', {
  state: () => ({
    shopId: '',
    shopName: '',
    shops: [],
  }),
  actions: {
    setShop(id, name) {
      this.shopId = id
      this.shopName = name
    },
    setShops(list) {
      this.shops = list
    },
  },
})
