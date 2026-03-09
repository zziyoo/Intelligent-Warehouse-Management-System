import json
import os

class WarehouseManager:
    def __init__(self):
        self.data_file = 'warehouse_data.json'
        self.items = self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)
    
    def add_item(self, name, quantity, category):
        item = {
            'id': len(self.items) + 1,
            'name': name,
            'quantity': quantity,
            'category': category
        }
        self.items.append(item)
        self.save_data()
        print(f"商品 {name} 已添加成功！")
    
    def view_items(self):
        if not self.items:
            print("仓库为空！")
            return
        
        print("\n=== 仓库商品列表 ===")
        print(f"{'ID':<5} {'名称':<20} {'数量':<10} {'分类':<15}")
        print("-" * 50)
        for item in self.items:
            print(f"{item['id']:<5} {item['name']:<20} {item['quantity']:<10} {item['category']:<15}")
        print("-" * 50)
    
    def update_item(self, item_id, new_quantity):
        for item in self.items:
            if item['id'] == item_id:
                item['quantity'] = new_quantity
                self.save_data()
                print(f"商品 ID {item_id} 数量已更新为 {new_quantity}！")
                return
        print(f"未找到 ID 为 {item_id} 的商品！")
    
    def delete_item(self, item_id):
        for i, item in enumerate(self.items):
            if item['id'] == item_id:
                deleted_item = self.items.pop(i)
                self.save_data()
                print(f"商品 {deleted_item['name']} 已删除！")
                return
        print(f"未找到 ID 为 {item_id} 的商品！")
    
    def search_item(self, keyword):
        results = []
        for item in self.items:
            if keyword.lower() in item['name'].lower() or keyword.lower() in item['category'].lower():
                results.append(item)
        
        if not results:
            print(f"未找到包含 '{keyword}' 的商品！")
            return
        
        print(f"\n=== 搜索结果 (包含 '{keyword}') ===")
        print(f"{'ID':<5} {'名称':<20} {'数量':<10} {'分类':<15}")
        print("-" * 50)
        for item in results:
            print(f"{item['id']:<5} {item['name']:<20} {item['quantity']:<10} {item['category']:<15}")
        print("-" * 50)
    
    def run(self):
        while True:
            print("\n=== 仓库管理系统 ===")
            print("1. 添加商品")
            print("2. 查看商品列表")
            print("3. 更新商品数量")
            print("4. 删除商品")
            print("5. 搜索商品")
            print("6. 退出系统")
            
            choice = input("请选择操作 (1-6): ")
            
            if choice == '1':
                name = input("请输入商品名称: ")
                quantity = int(input("请输入商品数量: "))
                category = input("请输入商品分类: ")
                self.add_item(name, quantity, category)
            
            elif choice == '2':
                self.view_items()
            
            elif choice == '3':
                item_id = int(input("请输入商品ID: "))
                new_quantity = int(input("请输入新的数量: "))
                self.update_item(item_id, new_quantity)
            
            elif choice == '4':
                item_id = int(input("请输入商品ID: "))
                self.delete_item(item_id)
            
            elif choice == '5':
                keyword = input("请输入搜索关键词: ")
                self.search_item(keyword)
            
            elif choice == '6':
                print("感谢使用仓库管理系统，再见！")
                break
            
            else:
                print("输入错误，请重新选择！")

if __name__ == "__main__":
    manager = WarehouseManager()
    manager.run()
