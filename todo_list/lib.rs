#![cfg_attr(not(feature = "std"), no_std)]


#[ink::contract]
mod todo_list {
    use ink_prelude::string::String;
    use ink_prelude::vec::Vec;
    use ink::storage::Mapping;
    use ink_env::debug_println;

    /// Defines the storage of your contract.
    /// Add new fields to the below struct in order
    /// to add new static storage fields to your contract.
    #[ink(storage)]
    pub struct TodoList {
        // Vec stores <Owner: AccountId, Alias: String>
        task: Mapping<String, Vec<(AccountId, String)>>,
        name: Vec<String>,
        // owner: AccountId,
        // alias: String,
        // value: bool,
        // task: String,
    }

    impl TodoList {
        /// Constructor that initializes the `bool` value to the given `init_value`.

        /// Constructor that initializes the `bool` value to `false`.
        ///
        /// Constructors can delegate to other constructors.
        #[ink(constructor)]
        pub fn default() -> Self {
            Self {
                task: Mapping::new(),
                name: Vec::new()
            }
        }

        /// Create task
        #[ink(message)]
        #[ink(payable)]
        pub fn create_task(&mut self, init_alias: String, init_task: String) -> Result<(String, String), String>  {
            
            let _task = init_task.clone();

            // Using task name, check if task exist
            let _task_list = self.task.get(&_task);

            // If exist, return task exist
            if let Some(_list) = _task_list {
                
                // return (String::from("TASK EXIST"), _task);
                return Err(String::from("Task already exists"));
            } 

            // Else create new task and store in hashmap
            else {
                let mut new_list = Vec::new();
                new_list.push((self.env().caller(), init_alias.clone())); // Store accountID & alias
                
                // Store in the format hashmap.insert(string, vec)
                self.task.insert(_task.clone(), &new_list);
                
                // Store alias into name vec
                self.name.push(_task.clone());

                return Ok((init_alias, _task));
            }
        }

        /// Remove task
        #[ink(message)]
        pub fn remove_task(&mut self, _task: String){
            assert!(self.only_owner(_task.clone()));
            self.task.remove(_task.clone());
            self.name.retain(|x| x != &_task);
        }

        /// Modify task
        #[ink(message)]
        pub fn modify_task(&mut self, _task: String, new_task: String) -> bool{
            assert!(self.only_owner(_task.clone()));
            let info = self.task.get(_task.clone());
            match info {
                Some(element) => {
                    let _alias = (element[0].1).clone();
                    self.task.remove(_task.clone());
                    self.name.retain(|x| x != &_task);
                    self.create_task(_alias.clone(), new_task.clone());
                    true
                },
                None => false
            }
        }
        
        /// Check if owner
        fn only_owner(&self, _task: String) -> bool {
            let info = self.task.get(_task);
            match info{
                Some(element) => self.env().caller() == element[0].0,
                None => false
            }
            
        }

        /// Return all information from sender
        #[ink(message)]
        pub fn get_all(&self, _task: String) -> Option<(String, AccountId, String)> {
            let task = self.task.get(_task.clone());
            match task {
                Some(element) => Some((_task.clone(), element[0].0, (element[0].1).clone())),
                None => None,
            }
        }

        /// Return all task
        #[ink(message)]
        pub fn get_all_task(&self) -> Vec<(String, Vec<(AccountId, String)>)> {
            let mut _tasks = Vec::new();
            for key in self.name.iter() {
                let value = self.task.get(key).unwrap();
                _tasks.push((key.clone(), value.clone()));
            }
            _tasks
        }

        /// Return owner
        #[ink(message)]
        pub fn get_owner(&self, _task: String) -> Option<AccountId> {
            let task = self.task.get(_task.clone());
            match task {
                Some(element) => Some(element[0].0),
                None => None
            }
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
            let mut todo_list = TodoList::default();
            let _task = String::from("clean floor");
            let _alias = String::from("alice");
            assert_eq!(todo_list.create_task(_alias.clone(),_task.clone()).unwrap(), 
                                            (_alias.clone(),_task.clone()));

            assert_eq!(todo_list.create_task(_alias.clone(),_task.clone()).unwrap_err(),
                                            String::from("Task already exists"));
        }

        /// Test task deletion
        #[ink::test]
        fn remove_task() {
            let mut todo_list = TodoList::default();
            let _task = String::from("clean floor");
            let _alias = String::from("alice");
            assert_eq!(todo_list.create_task(_alias.clone(),_task.clone()).unwrap(), 
                                            (_alias.clone(),_task.clone()));

            let before_result = todo_list.get_owner(_task.clone());
            let mut _owner_id: AccountId = before_result.unwrap();

            todo_list.remove_task(_task.clone());
            let after_result = todo_list.get_all(_task.clone());
            match after_result{
                Some((taskname, owner_id, alias)) => {
                        assert_ne!(((_task == taskname) && (_owner_id == owner_id) && (_alias == alias)), true)
                },
                None => assert_eq!(after_result, None),
            }
        }

        // Test modify task
        #[ink::test]
        fn modify_task() {
            let mut todo_list = TodoList::default();
            let _task = String::from("clean floor");
            let _alias = String::from("alice");
            assert_eq!(todo_list.create_task(_alias.clone(),_task.clone()).unwrap(), 
                                            (_alias.clone(),_task.clone()));
            
            let before_result = todo_list.get_all(_task.clone());
            let mut _before_task: String;
            match before_result{
                Some((taskname, owner_id, alias)) => {
                        _before_task = taskname;
                },
                None => assert_ne!(before_result, None),
            }

            let _new_task = String::from("pack the storeroom");
            todo_list.modify_task(_task.clone(), _new_task.clone());

            let after_result = todo_list.get_all(_new_task.clone());
            let mut _after_task: String;
            match after_result{
                Some((taskname, owner_id, alias)) => {
                    assert_eq!(taskname == _new_task, true);
                },
                None => {
                    assert_ne!(after_result, None);
                },
            }
        }

        // Test get all task
        #[ink::test]
        fn get_all_task() {
            let mut todo_list = TodoList::default();
            let _task = String::from("clean floor");
            let _alias = String::from("alice");
            assert_eq!(todo_list.create_task(String::from("alice"),String::from("clean floor")).unwrap(), 
                                            (String::from("alice"),String::from("clean floor")));

            let caller: AccountId = ink::env::test::default_accounts::<ink::env::DefaultEnvironment>()
                                    .bob;
            ink::env::test::set_caller::<ink::env::DefaultEnvironment>(caller);

            assert_eq!(todo_list.create_task(String::from("bob"),String::from("wash pan")).unwrap(), 
                                            (String::from("bob"),String::from("wash pan")));

            let caller: AccountId = ink::env::test::default_accounts::<ink::env::DefaultEnvironment>()
                                    .charlie;
            ink::env::test::set_caller::<ink::env::DefaultEnvironment>(caller);

            assert_eq!(todo_list.create_task(String::from("charlie"),String::from("pack clothes")).unwrap(), 
                                            (String::from("charlie"),String::from("pack clothes")));

            let _task_vec = todo_list.get_all_task();
            match _task_vec{
                _task_vec => {
                    for key in _task_vec.iter(){
                        let taskname = todo_list.get_all(key.0.clone());
                        if let Some((task, owner_id, alias)) = taskname{ 
                            debug_println!("{}", alias);
                            assert_eq!(task == key.0.clone() && owner_id == key.1[0].0 && alias == key.1[0].1, true)
                        }
                   }
                }
            }

        }

        // Test owner access
        #[ink::test]
        #[should_panic]
        fn only_owner_access() {
            let mut todo_list = TodoList::default();
            let _task = String::from("clean floor");
            let _alias = String::from("alice");
            assert_eq!(todo_list.create_task(_alias.clone(),_task.clone()).unwrap(), 
                                            (_alias.clone(),_task.clone()));
            
            
            let caller: AccountId = ink::env::test::default_accounts::<ink::env::DefaultEnvironment>()
                .bob;
            ink::env::test::set_caller::<ink::env::DefaultEnvironment>(caller);

            // println!("Owner = {}", format!( "{:?} ", todo_list.get_owner()));
            // println!("Caller = {:?}", caller);
            todo_list.modify_task(_task.clone(), String::from("Wash the clothes"));
        }
        
    }
}