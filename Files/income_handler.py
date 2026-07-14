"""
Income Handler Module - Manages income operations
"""

import json
import os
from datetime import datetime
import uuid


class IncomeHandler:
    """Handles all income file operations"""

    def __init__(self, file_path="data/incomes.json"):
        self.file_path = file_path
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Create the JSON file if it doesn't exist"""
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            if not os.path.exists(self.file_path):
                with open(self.file_path, 'w') as file:
                    json.dump([], file, indent=4)
                print("✅ Incomes file created successfully!")
        except Exception as e:
            print(f"❌ Error creating incomes file: {e}")

    def read_incomes(self, start_date=None, end_date=None):
        """Read all incomes with optional date filters"""
        try:
            with open(self.file_path, 'r') as file:
                incomes = json.load(file)

            if start_date:
                incomes = [i for i in incomes if i.get('date', '') >= start_date]
            if end_date:
                incomes = [i for i in incomes if i.get('date', '') <= end_date]

            return incomes
        except Exception as e:
            print(f"❌ Error reading incomes: {e}")
            return []

    def write_incomes(self, incomes):
        """Write incomes to file"""
        try:
            with open(self.file_path, 'w') as file:
                json.dump(incomes, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error writing incomes: {e}")
            return False

    def add_income(self, source, amount, description, date=None, is_recurring=False, frequency=None):
        """Add a new income"""
        try:
            if not amount or float(amount) <= 0:
                raise ValueError("Amount must be greater than 0")
            if not source or not source.strip():
                raise ValueError("Source is required")

            incomes = self.read_incomes()

            if date is None or date == '':
                date = datetime.now().strftime("%Y-%m-%d")

            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                date = datetime.now().strftime("%Y-%m-%d")

            new_income = {
                "id": str(uuid.uuid4())[:8],
                "source": source.strip(),
                "amount": float(amount),
                "description": description.strip() if description else "",
                "date": date,
                "is_recurring": is_recurring,
                "frequency": frequency if is_recurring else None,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            incomes.append(new_income)
            success = self.write_incomes(incomes)

            if success:
                print(f"✅ Income added: {source} - ${amount}")
                return new_income
            return None
        except Exception as e:
            print(f"❌ Error adding income: {e}")
            return None

    def update_income(self, income_id, source=None, amount=None, description=None, date=None, is_recurring=None,
                      frequency=None):
        """Update an existing income"""
        try:
            incomes = self.read_incomes()
            income_found = None
            for income in incomes:
                if income['id'] == income_id:
                    income_found = income
                    break

            if not income_found:
                return False

            if source is not None and source.strip():
                income_found['source'] = source.strip()
            if amount is not None:
                if float(amount) <= 0:
                    raise ValueError("Amount must be greater than 0")
                income_found['amount'] = float(amount)
            if description is not None:
                income_found['description'] = description.strip() if description else ""
            if date is not None and date != '':
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    income_found['date'] = date
                except ValueError:
                    pass
            if is_recurring is not None:
                income_found['is_recurring'] = is_recurring
                income_found['frequency'] = frequency if is_recurring else None

            success = self.write_incomes(incomes)
            return success
        except Exception as e:
            print(f"❌ Error updating income: {e}")
            return False

    def delete_income(self, income_id):
        """Delete an income by ID"""
        try:
            incomes = self.read_incomes()
            original_length = len(incomes)
            updated_incomes = [i for i in incomes if i['id'] != income_id]

            if len(updated_incomes) == original_length:
                return False

            success = self.write_incomes(updated_incomes)
            return success
        except Exception as e:
            print(f"❌ Error deleting income: {e}")
            return False

    def get_income_by_id(self, income_id):
        """Get a single income by ID"""
        try:
            incomes = self.read_incomes()
            for income in incomes:
                if income['id'] == income_id:
                    return income
            return None
        except Exception as e:
            print(f"❌ Error finding income: {e}")
            return None

    def get_total_income(self, start_date=None, end_date=None):
        """Calculate total income"""
        try:
            incomes = self.read_incomes(start_date, end_date)
            total = sum(income['amount'] for income in incomes)
            return round(total, 2)
        except Exception as e:
            print(f"❌ Error calculating total income: {e}")
            return 0

    def get_monthly_income(self, year=None, month=None):
        """Get income summary for a specific month"""
        try:
            if year is None:
                year = datetime.now().year
            if month is None:
                month = datetime.now().month

            incomes = self.read_incomes()
            filtered = []
            for income in incomes:
                try:
                    income_date = datetime.strptime(income['date'], "%Y-%m-%d")
                    if income_date.year == year and income_date.month == month:
                        filtered.append(income)
                except ValueError:
                    continue

            total = sum(i['amount'] for i in filtered)

            return {
                'total': round(total, 2),
                'count': len(filtered),
                'incomes': filtered
            }
        except Exception as e:
            print(f"❌ Error getting monthly income: {e}")
            return {'total': 0, 'count': 0, 'incomes': []}

    def get_income_by_source(self):
        """Group income by source"""
        try:
            incomes = self.read_incomes()
            sources = {}
            for income in incomes:
                source = income['source']
                if source in sources:
                    sources[source] += income['amount']
                else:
                    sources[source] = income['amount']
            for source in sources:
                sources[source] = round(sources[source], 2)
            return sources
        except Exception as e:
            print(f"❌ Error grouping income: {e}")
            return {}

    def get_net_savings(self, month=None, year=None):
        """Calculate net savings (income - expenses)"""
        try:
            from utils.file_handler import FileHandler
            expense_handler = FileHandler()

            if month is None:
                month = datetime.now().month
            if year is None:
                year = datetime.now().year

            monthly_income = self.get_monthly_income(year, month)
            monthly_expenses = expense_handler.get_monthly_summary(year, month)

            total_income = monthly_income.get('total', 0)
            total_expenses = monthly_expenses.get('total', 0)

            return {
                'total_income': total_income,
                'total_expenses': total_expenses,
                'net_savings': round(total_income - total_expenses, 2)
            }
        except Exception as e:
            print(f"❌ Error calculating net savings: {e}")
            return {'total_income': 0, 'total_expenses': 0, 'net_savings': 0}