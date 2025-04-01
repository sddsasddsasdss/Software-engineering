import datetime
import time # Used for simulating time passing in tests

class InsufficientFundsError(Exception):
  """Custom exception for insufficient funds."""
  pass

class AccountClosedError(Exception):
  """Custom exception for operations on a closed account."""
  pass

class AccountInactiveError(Exception):
  """Custom exception for operations on an inactive account before reactivation."""
  # Although reactivation happens automatically, this could be raised
  # if an external check wants to differentiate. For simplicity,
  # we might not explicitly raise this in basic operations.
  pass

class VerificationRequiredError(Exception):
  """Custom exception when withdrawal requires verification."""
  pass

class BankAccount:
  """
  Manages funds in a bank account with deposit, withdrawal,
  closing, and activation features.
  """

  # Define the inactivity period in seconds (e.g., 30 days)
  # For testing purposes, we might use a shorter duration.
  # INACTIVITY_PERIOD_SECONDS = 30 * 24 * 60 * 60 # 30 days
  INACTIVITY_PERIOD_SECONDS = 10 # Shorter duration for easier testing

  def __init__(self, initial_balance=0.0, account_holder="Unknown"):
    """
    Initializes the bank account.

    Args:
        initial_balance (float): The starting balance. Defaults to 0.0.
        account_holder (str): The name of the account holder.
    """
    if initial_balance < 0:
        raise ValueError("Initial balance cannot be negative.")

    self._balance = float(initial_balance)
    self._account_holder = account_holder
    self._is_active = True
    self._is_closed = False
    # Store the timestamp of the last operation
    self._last_activity_time = datetime.datetime.now()
    print(f"Account for {self._account_holder} created with balance: ${self._balance:.2f}")

  @property
  def balance(self):
    """Returns the current account balance."""
    # Optionally check status before allowing balance check
    # self._check_status_for_read()
    return self._balance

  @property
  def is_active(self):
    """Returns True if the account is active, False otherwise."""
    return self._is_active

  @property
  def is_closed(self):
    """Returns True if the account is closed, False otherwise."""
    return self._is_closed

  @property
  def account_holder(self):
    """Returns the name of the account holder."""
    return self._account_holder

  @property
  def last_activity_time(self):
    """Returns the timestamp of the last activity."""
    return self._last_activity_time

  def _update_activity_time(self):
    """Updates the last activity timestamp."""
    self._last_activity_time = datetime.datetime.now()

  def _check_status_for_operation(self):
    """
    Checks if the account is closed or inactive before performing an operation.
    Reactivates the account if it was inactive.
    Raises errors if closed.
    """
    if self._is_closed:
      raise AccountClosedError("Operation failed: Account is permanently closed.")

    if not self._is_active:
      self._reactivate() # Reactivate on operation attempt

  def _reactivate(self):
    """Reactivates the account and triggers the associated action."""
    if not self._is_active and not self._is_closed:
      self._is_active = True
      self._trigger_reactivation_action()
      # Update activity time upon reactivation itself? Or rely on the operation?
      # Let's rely on the operation updating it.

  def _trigger_reactivation_action(self):
    """Placeholder for the action taken upon account reactivation."""
    # In a real system, this could send an email, SMS, or log the event.
    print(f"Account for {self._account_holder} has been reactivated.")

  def deposit(self, amount):
    """
    Deposits funds into the account. Always possible unless the account is closed.

    Args:
        amount (float): The amount to deposit. Must be positive.

    Raises:
        ValueError: If the amount is not positive.
        AccountClosedError: If the account is closed.
    """
    if amount <= 0:
      raise ValueError("Deposit amount must be positive.")

    # Check status *before* proceeding
    self._check_status_for_operation() # This will reactivate if needed

    self._balance += amount
    self._update_activity_time()
    print(f"Deposited ${amount:.2f}. New balance: ${self._balance:.2f}")

  def withdraw(self, amount, is_verified=False):
    """
    Withdraws funds from the account after identity verification.

    Args:
        amount (float): The amount to withdraw. Must be positive.
        is_verified (bool): Flag indicating if the client's identity has been verified.

    Raises:
        ValueError: If the amount is not positive.
        VerificationRequiredError: If identity is not verified.
        AccountClosedError: If the account is closed.
        InsufficientFundsError: If the amount exceeds the balance.
    """
    if amount <= 0:
      raise ValueError("Withdrawal amount must be positive.")

    # 1. Check verification first, as per requirement 1
    if not is_verified:
      raise VerificationRequiredError("Withdrawal requires client identity verification.")

    # 2. Check account status (closed/inactive)
    self._check_status_for_operation() # This will reactivate if needed

    # 3. Check funds
    if amount > self._balance:
      raise InsufficientFundsError(f"Withdrawal failed: Insufficient funds. Available: ${self._balance:.2f}")

    # 4. Perform withdrawal
    self._balance -= amount
    self._update_activity_time()
    print(f"Withdrew ${amount:.2f}. New balance: ${self._balance:.2f}")

  def close_account(self):
    """
    Permanently closes the account. Operations will no longer be possible.
    """
    if self._is_closed:
      print("Account is already closed.")
      return

    # Potentially add checks here, e.g., balance must be zero before closing.
    # For now, just marking as closed.
    self._is_closed = True
    self._is_active = False # A closed account is implicitly inactive
    print(f"Account for {self._account_holder} has been closed.")
    # Should we clear the balance on close? Depends on requirements.
    # self._balance = 0.0

  def check_for_deactivation(self):
      """
      Checks if the account should be deactivated based on the inactivity period.
      This method would typically be called by an external process or scheduler.
      """
      if not self._is_active or self._is_closed:
          return # Already inactive or closed

      time_since_last_activity = datetime.datetime.now() - self._last_activity_time
      if time_since_last_activity.total_seconds() > self.INACTIVITY_PERIOD_SECONDS:
          self._deactivate()

  def _deactivate(self):
      """Marks the account as inactive."""
      if self._is_active and not self._is_closed:
          self._is_active = False
          print(f"Account for {self._account_holder} has been deactivated due to inactivity.")

  # --- Helper methods primarily for testing ---
  def force_deactivate(self):
      """Manually forces the account to be inactive (for testing)."""
      if not self._is_closed:
          self._is_active = False
          print(f"Account for {self._account_holder} manually set to inactive.")

  def set_last_activity_time(self, dt):
      """Manually sets the last activity time (for testing inactivity)."""
      if isinstance(dt, datetime.datetime):
          self._last_activity_time = dt
      else:
          raise TypeError("dt must be a datetime.datetime object")


# Example Usage (Optional - primarily tested via unit tests)
try:
    # Changed "Alice" to "Saka" here
    acc = BankAccount(100, "Saka")
    acc.deposit(50)
    acc.withdraw(30, is_verified=True)
    # acc.withdraw(10, is_verified=False) # Raises VerificationRequiredError
    # acc.withdraw(200, is_verified=True) # Raises InsufficientFundsError

    # Simulate inactivity for testing deactivation/reactivation
    print("\nSimulating inactivity...")
    # Backdate last activity time significantly for testing check_for_deactivation
    # Use the short INACTIVITY_PERIOD_SECONDS defined above for this example to work quickly
    past_time = datetime.datetime.now() - datetime.timedelta(seconds=BankAccount.INACTIVITY_PERIOD_SECONDS + 1)
    acc.set_last_activity_time(past_time)
    print(f"Set last activity time to: {acc.last_activity_time}")
    acc.check_for_deactivation() # Manually trigger the check
    print(f"Account active after check: {acc.is_active}")

    # Wait a moment to ensure the check_for_deactivation logic has time if run concurrently
    # time.sleep(0.1) # Usually not needed unless INACTIVITY_PERIOD_SECONDS is extremely short

    print("\nAttempting deposit on (now potentially) inactive account...")
    acc.deposit(10) # Should reactivate if inactive, then deposit
    print(f"Account active after deposit: {acc.is_active}")
    print(f"Current balance: ${acc.balance:.2f}")


    print("\nClosing account...")
    acc.close_account()
    # acc.deposit(5) # Raises AccountClosedError

except (ValueError, InsufficientFundsError, AccountClosedError, VerificationRequiredError) as e:
    print(f"Error: {e}")
