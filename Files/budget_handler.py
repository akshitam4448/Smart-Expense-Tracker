"""
Budget Handler Module - Manages budget operations
"""

import json
import os
from datetime import datetime
import uuid


class BudgetHandler:
    """Handles all budget file operations"""

    def __init__(self, file_path="data/budgets.json"):
        self.file_path = file_path
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Create the JSON file if it doesn't exist"""
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            if not os.path.exists(self.file_path):
                with open(self.file_path, 'w') as file:
                    json.dump([], file, indent=4)
                print("✅ Budgets file created successfully!")
            else:
                # Verify file is valid JSON
                try:
                    with open(self.file_path, 'r') as file:
                        json.load(file)
                except json.JSONDecodeError:
                    # If file is corrupted, reset it
                    with open(self.file_path, 'w') as file:
                        json.dump([], file, indent=4)
                    print("⚠️ Budgets file was corrupted! Reset to empty.")
        except Exception as e:
            print(f"❌ Error creating budgets file: {e}")

    def read_budgets(self):
        """Read all budgets"""
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except FileNotFoundError:
            self.ensure_file_exists()
            return []
        except json.JSONDecodeError:
            print("⚠️ Budgets file corrupted! Starting with empty.")
            return []
        except Exception as e:
            print(f"❌ Error reading budgets: {e}")
            return []

    def write_budgets(self, budgets):
        """Write budgets to file"""
        try:
            with open(self.file_path, 'w') as file:
                json.dump(budgets, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error writing budgets: {e}")
            return False

    def add_budget(self, category, amount, month=None, year=None):
        """Add a new budget"""
        try:
            # Validate input
            if not category or not category.strip():
                raise ValueError("Category is required")
            if not amount or float(amount) <= 0:
                raise ValueError("Budget amount must be greater than 0")

            # Get current month/year if not provided
            if month is None:
                month = datetime.now().month
            if year is None:
                year = datetime.now().year

            # Convert to int
            month = int(month)
            year = int(year)

            # Read existing budgets
            budgets = self.read_budgets()

            # Check if budget already exists for this category/month
            for budget in budgets:
                if (budget.get('category', '').lower() == category.strip().lower() and
                        budget.get('month') == month and
                        budget.get('year') == year):
                    raise ValueError(f"Budget already exists for {category} in this month")

            # Create new budget
            new_budget = {
                "id": str(uuid.uuid4())[:8],
                "category": category.strip(),
                "amount": float(amount),
                "month": month,
                "year": year,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Add and save
            budgets.append(new_budget)
            success = self.write_budgets(budgets)

            if success:
                print(f"✅ Budget added: {category} - ${amount} for {month}/{year}")
                return new_budget
            return None

        except ValueError as e:
            print(f"❌ Validation error: {e}")
            raise
        except Exception as e:
            print(f"❌ Error adding budget: {e}")
            return None

    def update_budget(self, budget_id, category=None, amount=None):
        """Update an existing budget"""
        try:
            budgets = self.read_budgets()
            budget_found = None
            index = -1

            for i, budget in enumerate(budgets):
                if budget.get('id') == budget_id:
                    budget_found = budget
                    index = i
                    break

            if not budget_found:
                print(f"⚠️ Budget with ID {budget_id} not found")
                return False

            # Update fields
            if category is not None and category.strip():
                budget_found['category'] = category.strip()
            if amount is not None:
                if float(amount) <= 0:
                    raise ValueError("Budget amount must be greater than 0")
                budget_found['amount'] = float(amount)

            # Save updated list
            budgets[index] = budget_found
            success = self.write_budgets(budgets)

            if success:
                print(f"✅ Budget {budget_id} updated successfully")
                return True
            return False

        except ValueError as e:
            print(f"❌ Validation error: {e}")
            raise
        except Exception as e:
            print(f"❌ Error updating budget: {e}")
            return False

    def delete_budget(self, budget_id):
        """Delete a budget by ID"""
        try:
            budgets = self.read_budgets()
            original_length = len(budgets)
            updated_budgets = [b for b in budgets if b.get('id') != budget_id]

            if len(updated_budgets) == original_length:
                print(f"⚠️ Budget with ID {budget_id} not found")
                return False

            success = self.write_budgets(updated_budgets)
            if success:
                print(f"✅ Budget {budget_id} deleted successfully")
                return True
            return False

        except Exception as e:
            print(f"❌ Error deleting budget: {e}")
            return False

    def get_budget_by_id(self, budget_id):
        """Get a single budget by ID"""
        try:
            budgets = self.read_budgets()
            for budget in budgets:
                if budget.get('id') == budget_id:
                    return budget
            return None
        except Exception as e:
            print(f"❌ Error finding budget: {e}")
            return None

    def get_budget_by_category(self, category, month=None, year=None):
        """Get budget for a specific category and month"""
        try:
            if month is None:
                month = datetime.now().month
            if year is None:
                year = datetime.now().year

            budgets = self.read_budgets()
            for budget in budgets:
                if (budget.get('category', '').lower() == category.lower() and
                        budget.get('month') == month and
                        budget.get('year') == year):
                    return budget
            return None
        except Exception as e:
            print(f"❌ Error finding budget: {e}")
            return None

    def get_all_budgets_for_month(self, month=None, year=None):
        """Get all budgets for a specific month"""
        try:
            if month is None:
                month = datetime.now().month
            if year is None:
                year = datetime.now().year

            budgets = self.read_budgets()
            result = [b for b in budgets if b.get('month') == month and b.get('year') == year]
            print(f"📊 Found {len(result)} budgets for {month}/{year}")
            return result

        except Exception as e:
            print(f"❌ Error getting budgets: {e}")
            return []

    def get_budget_status(self, month=None, year=None):
        """Get budget status with actual spending"""
        try:
            if month is None:
                month = datetime.now().month
            if year is None:
                year = datetime.now().year

            budgets = self.get_all_budgets_for_month(month, year)
            if not budgets:
                print(f"ℹ️ No budgets found for {month}/{year}")
                return []

            # Get actual expenses for the month
            from utils.file_handler import FileHandler
            expense_handler = FileHandler()
            monthly_expenses = expense_handler.get_monthly_summary(year, month)
            expense_categories = monthly_expenses.get('categories', {})

            status = []
            for budget in budgets:
                category = budget.get('category', '')
                budget_amount = budget.get('amount', 0)
                actual_amount = expense_categories.get(category, 0)

                percentage = (actual_amount / budget_amount * 100) if budget_amount > 0 else 0
                remaining = budget_amount - actual_amount
                is_over_budget = actual_amount > budget_amount

                status.append({
                    'id': budget.get('id'),
                    'category': category,
                    'budget': budget_amount,
                    'actual': actual_amount,
                    'remaining': round(remaining, 2),
                    'percentage': round(percentage, 2),
                    'is_over_budget': is_over_budget,
                    'status': 'over' if is_over_budget else 'under'
                })

            return status

        except Exception as e:
            print(f"❌ Error getting budget status: {e}")
            return []

    def get_total_budget_for_month(self, month=None, year=None):
        """Get total budget for a month"""
        try:
            if month is None:
                month = datetime.now().month
            if year is None:
                year = datetime.now().year

            budgets = self.get_all_budgets_for_month(month, year)
            total = sum(b.get('amount', 0) for b in budgets)
            return round(total, 2)

        except Exception as e:
            print(f"❌ Error getting total budget: {e}")
            return 0