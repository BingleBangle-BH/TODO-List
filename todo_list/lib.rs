#![cfg_attr(not(feature = "std"), no_std)]


#[ink::contract]
mod todo_list {
    use ink_prelude::string::String;
    /// Defines the storage of your contract.
    /// Add new fields to the below struct in order
    /// to add new static storage fields to your contract.
    #[ink(storage)]
    pub struct TodoList {
        /// Stores a single `bool` value on the storage.
        owner: AccountId,
        value: bool,
        task: String,
    }


    impl TodoList {
        /// Constructor that initializes the `bool` value to the given `init_value`.
        #[ink(constructor)]
        pub fn new(init_value: bool, init_task: String) -> Self {
            Self { 
                owner: Self::env().caller(),
                value: init_value,
                task: init_task,
            }
        }

        /// Constructor that initializes the `bool` value to `false`.
        ///
        /// Constructors can delegate to other constructors.
        #[ink(constructor)]
        pub fn default() -> Self {
            Self::new(Default::default(), String::default())
        }

        /// A message that can be called on instantiated contracts.
        /// This one flips the value of the stored `bool` from `true`
        /// to `false` and vice versa.
        #[ink(message)]
        pub fn flip(&mut self) {
            self.value = !self.value;
        }

        /// Return task
        #[ink(message)]
        pub fn get_task(&self) -> String {
            self.task.clone()
        }

        /// Return owner
        #[ink(message)]
        pub fn get_owner(&self) -> AccountId {
            self.owner
        }

        /// Modify task
        #[ink(message)]
        pub fn modify_task(&mut self, new_task: String){
            assert!(self.only_owner());
            self.task = new_task;
        }

        fn only_owner(&self) -> bool {
            self.env().caller() == self.owner
        }
    }

    /// Unit tests in Rust are normally defined within such a `#[cfg(test)]`
    /// module and test functions are marked with a `#[test]` attribute.
    /// The below code is technically just normal Rust code.
    #[cfg(test)]
    mod tests {
        /// Imports all the definitions from the outer scope so we can use them here.
        use super::*;

        /// We test if the default constructor does its job.
        #[ink::test]
        fn default_works() {
            let todo_list = TodoList::default();
            assert_eq!(todo_list.get_task(), "");
        }

        /// We test a simple use case of our contract.
        #[ink::test]
        fn it_works() {
            let mut todo_list = TodoList::new(false, String::from("Clean the toilet"));
            assert_eq!(todo_list.get_task(), "Clean the toilet");
            todo_list.modify_task(String::from("Wash the clothes"));
            assert_eq!(todo_list.get_task(), "Wash the clothes");
            ink::env::debug_println!("test");
            // println!("{}", format!( "{:#?} ", todo_list.get_owner()));
        }
    }
}
