# Software-engineering
 Online Banking class created using python which will manage the funds collected in a bank account  

The requirements:
The client asked to create a class that will manage the funds collected in a bank account. The class will initially provide two operations: depositing new funds and withdrawing collected funds.
During the implementation, additional requirements appeared:
1. Depositing funds will always be possible. The operation of withdrawing funds can take place after initial verification of the client's identity (e.g. verification of an identity document)
2. The account owner will be able to close it. After closing the account, operations on it will not be possible
3. The account can be deactivated if there are no operations on it for a certain period of time 4. The account will be reactivated after an operation appears on it (deposit or withdrawal of funds)
5. Reactivation of the account will trigger an additional action (undefined), e.g. sending a message that the account has been reactivated
Tasks:
1. Prepare the implementation in accordance with the above requirements. The implementation should be performed using an object-oriented programming language
2. Develop tests for the created class: start conditions and execution result. Tests should cover all execution paths
3. Based on point 2, create unit tests of the implemented class
