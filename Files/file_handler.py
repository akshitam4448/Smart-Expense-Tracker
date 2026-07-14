"""
File Handler Module - Manages all JSON file operations for expenses
"""

import json
import os
from datetime import datetime
import uuid


class FileHandler:
    """Handles all expense file operations"""

    def __init__(self, file_path="data/expenses.json"):
        self.file_path = file_path
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Create the JSON file if it doesn't exist"""
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            if not os.path.exists(self.file_path):
                with open(self.file_path, 'w') as file:
                    json.dump([], file, indent=4)
                print("✅ Expenses file created successfully!")
        except Exception as e:
            print(f"❌ Error creating file: {e}")

    def read_expenses(self, category=None, start_date=None, end_date=None):
        """Read expenses with optional filters"""
        try:
            with open(self.file_path, 'r') as file:
                expenses = json.load(file)

            if category:
                expenses = [e for e in expenses if e.get('category', '').lower() == category.lower()]
            if start_date:
                expenses = [e for e in expenses if e.get('date', '') >= start_date]
            if end_date:
                expenses = [e for e in expenses if e.get('date', '') <= end_date]

            return expenses
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return []

    def write_expenses(self, expenses):
        """Write expenses to the JSON file"""
        try:
            with open(self.file_path, 'w') as file:
                json.dump(expenses, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error writing file: {e}")
            return False

    def add_expense(self, amount, category, description, date=None):
        """Add a new expense"""
        try:
            if not amount or float(amount) <= 0:
                raise ValueError("Amount must be greater than 0")
            if not category or not category.strip():
                raise ValueError("Category is required")
            if not description or not description.strip():
                raise ValueError("Description is required")

            expenses = self.read_expenses()

            if date is None or date == '':
                date = datetime.now().strftime("%Y-%m-%d")

            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                date = datetime.now().strftime("%Y-%m-%d")

            new_expense = {
                "id": str(uuid.uuid4())[:8],
                "amount": float(amount),
                "category": category.strip(),
                "description": description.strip(),
                "date": date,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            expenses.append(new_expense)
            success = self.write_expenses(expenses)

            if success:
                print(f"✅ Expense added: {description} - ${amount}")
                return new_expense
            return None
        except Exception as e:
            print(f"❌ Error adding expense: {e}")
            return None

    def update_expense(self, expense_id, amount=None, category=None, description=None, date=None):
        """Update an existing expense"""
        try:
            expenses = self.read_expenses()
            expense_found = None
            for expense in expenses:
                if expense['id'] == expense_id:
                    expense_found = expense
                    break

            if not expense_found:
                return False

            if amount is not None:
                if float(amount) <= 0:
                    raise ValueError("Amount must be greater than 0")
                expense_found['amount'] = float(amount)
            if category is not None and category.strip():
                expense_found['category'] = category.strip()
            if description is not None and description.strip():
                expense_found['description'] = description.strip()
            if date is not None and date != '':
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    expense_found['date'] = date
                except ValueError:
                    pass

            success = self.write_expenses(expenses)
            return success
        except Exception as e:
            print(f"❌ Error updating expense: {e}")
            return False

    def delete_expense(self, expense_id):
        """Delete an expense by ID"""
        try:
            expenses = self.read_expenses()
            original_length = len(expenses)
            updated_expenses = [e for e in expenses if e['id'] != expense_id]

            if len(updated_expenses) == original_length:
                return False

            success = self.write_expenses(updated_expenses)
            return success
        except Exception as e:
            print(f"❌ Error deleting expense: {e}")
            return False

    def get_expense_by_id(self, expense_id):
        """Get a single expense by ID"""
        try:
            expenses = self.read_expenses()
            for expense in expenses:
                if expense['id'] == expense_id:
                    return expense
            return None
        except Exception as e:
            print(f"❌ Error finding expense: {e}")
            return None

    def get_total_expenses(self, category=None):
        """Calculate total of all expenses"""
        try:
            expenses = self.read_expenses(category=category)
            total = sum(expense['amount'] for expense in expenses)
            return round(total, 2)
        except Exception as e:
            print(f"❌ Error calculating total: {e}")
            return 0

    def get_expenses_by_category(self):
        """Group expenses by category"""
        try:
            expenses = self.read_expenses()
            categories = {}
            for expense in expenses:
                category = expense['category']
                if category in categories:
                    categories[category] += expense['amount']
                else:
                    categories[category] = expense['amount']
            for category in categories:
                categories[category] = round(categories[category], 2)
            return categories
        except Exception as e:
            print(f"❌ Error grouping expenses: {e}")
            return {}

    def get_recent_expenses(self, limit=5):
        """Get the most recent expenses"""
        try:
            expenses = self.read_expenses()
            sorted_expenses = sorted(expenses, key=lambda x: x['date'], reverse=True)
            return sorted_expenses[:limit]
        except Exception as e:
            print(f"❌ Error getting recent expenses: {e}")
            return []

    def search_expenses(self, search_term):
        """Search expenses by description or category"""
        try:
            expenses = self.read_expenses()
            search_term = search_term.lower()
            results = [
                e for e in expenses
                if search_term in e['description'].lower()
                   or search_term in e['category'].lower()
            ]
            return results
        except Exception as e:
            print(f"❌ Error searching expenses: {e}")
            return []

    def get_monthly_summary(self, year=None, month=None):
        """Get expense summary for a specific month"""
        try:
            if year is None:
                year = datetime.now().year
            if month is None:
                month = datetime.now().month

            expenses = self.read_expenses()
            filtered = []
            for expense in expenses:
                try:
                    expense_date = datetime.strptime(expense['date'], "%Y-%m-%d")
                    if expense_date.year == year and expense_date.month == month:
                        filtered.append(expense)
                except ValueError:
                    continue

            total = sum(e['amount'] for e in filtered)
            categories = {}
            for expense in filtered:
                category = expense['category']
                if category in categories:
                    categories[category] += expense['amount']
                else:
                    categories[category] = expense['amount']

            return {
                'total': round(total, 2),
                'categories': categories,
                'count': len(filtered),
                'expenses': filtered
            }
        except Exception as e:
            print(f"❌ Error getting monthly summary: {e}")
            return {'total': 0, 'categories': {}, 'count': 0, 'expenses': []}

    def get_statistics(self):
        """Get comprehensive statistics"""
        try:
            expenses = self.read_expenses()
            if not expenses:
                return {
                    'total': 0,
                    'count': 0,
                    'average': 0,
                    'max': 0,
                    'min': 0,
                    'categories': {},
                    'monthly': {}
                }

            amounts = [e['amount'] for e in expenses]
            return {
                'total': round(sum(amounts), 2),
                'count': len(expenses),
                'average': round(sum(amounts) / len(amounts), 2),
                'max': max(amounts),
                'min': min(amounts),
                'categories': self.get_expenses_by_category(),
                'monthly': self.get_monthly_summary()
            }
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")
            return None