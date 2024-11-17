
post validate_user

url: users/validate

post register_user

url: users/register

```json
{
"user_name":"string",
"user_password":"string"
}

```
return: auth_token

........................................................

auth_token:

```json
{
	"user_id": "int",
	"user_type": "manager/user",
    
}
```

eventually might want to update "business_ids_whom_i_manage": [business_id_1, business_id_2]

........................................................

get show_order_classes_by_day

url: order_classes/{business_id}

HEADER: auth_token *user/*manager

```json
return: {
	"20-10-2025": [
		{"order_class_id": "int", "title": "str", "sellable_quantity": "int", "sold_quantity": "int"},
		{"order_class_id": "int", "title": "str", "sellable_quantity": "int", "sold_quantity": "int"},
		{"order_class_id": "int", "title": "str", "sellable_quantity": "int", "sold_quantity": "int"}
	],
	"21-10-2025": [
		{"order_class_id": "int", "title": "str", "sellable_quantity": "int", "sold_quantity": "int"},
		{"order_class_id": "int", "title": "str", "sellable_quantity": "int", "sold_quantity": "int"},
		{"order_class_id": "int", "title": "str", "sellable_quantity": "int", "sold_quantity": "int"}
	]
}
```

........................................................

post create_order_class

url: order_classes/{business_id}

HEADER: auth_token *manager

```json
{
	"title": "pao centeio",
	"delivery_date": 20-10-2025
}
return true/false
```


........................................................

put update_order_class

url: order_classes/{business_id}

HEADER: auth_token *manager

```json
{
	"order_id": "string",
	"sellable_quantity": "int"
}
return true/false
```

*check if new sellable_quantity < current sold_quantity, sends error if it's the case

........................................................

post create_order

url: orders/{business_id}

HEADER: auth_token *user

```json
{
	"order_date": "date",
	"state": "to_be_validated",
	"order_units": [
		{"order_class_id": "int", "quantity": "int"},
		{"order_class_id": "int", "quantity": "int"},
		{"order_class_id": "int", "quantity": "int"}
	]
}
```

........................................................

put update_order

url: orders/{business_id}

HEADER: auth_token *manager

```json
{
	"order_id": "int",
	"state": "to_be_delivered/delivered"
}
```

*if to_be_validated ->to_be_delivered, update the order_class sold_quantity

........................................................
get show_business_orders_by_date

endpoint: orders/{business_id}?filter="order_state"

HEADER: auth_token *manager

```json
return: {
	"20-10-2025": [
		{
			"order_id": "int",
			"order_info": [
				{"title": "str", "quantity": "int"},
				{"title": "str", "quantity": "int"},
				{"title": "str", "quantity": "int"},
			],
			"order_state": "str"
		},
		{
			"order_id": "int",
			"order_info": [
				{"title": "str", "quantity": "int"},
				{"title": "str", "quantity": "int"},
				{"title": "str", "quantity": "int"},
			],
			"order_state": "str"
		},
	],
	"21-10-2025": [
		{
			"order_id": "int",
			"order_info": [
				{"title": "str", "quantity": "int"},
				{"title": "str", "quantity": "int"},
				{"title": "str", "quantity": "int"},
			],
			"order_state": "str"
		},
		{
			"order_id": "int",
			"order_info": [
				{"title": "str", "quantity": "int"},
				{"title": "str", "quantity": "int"},
				{"title": "str", "quantity": "int"},
			],
			"order_state": "str"
		},
	]
}
```

........................................................
get show_users_orders_by_date

endpoint: orders/{business_id}/{user_id}?filter="order_state"

HEADER: auth_token *user/*manager

```json

return: {
	"20-10-2025": [
		{
			"order_id": "int",
			"order_info": [
				{"title": "str", "quantity": "int"},
				{"title": "str", "quantity": "int"},
				{"title": "str", "quantity": "int"},
			],
			"order_state": "str"
		},
		{
			"order_id": "int",
			"order_info": [
				{"title": "str", "quantity": "int"},
				{"title": "str", "quantity": "int"},
				{"title": "str", "quantity": "int"},
			],
			"order_state": "str"
		},
	],
	"21-10-2025": [
		{
			"order_id": "int",
			"order_info": [
				{"title": "str", "quantity": "int"},
				{"title": "str", "quantity": "int"},
				{"title": "str", "quantity": "int"},
			],
			"order_state": "str"
		},
		{
			"order_id": "int",
			"order_info": [
				{"title": "str", "quantity": "int"},
				{"title": "str", "quantity": "int"},
				{"title": "str", "quantity": "int"},
			],
			"order_state": "str"
		},
	]
}
```

***

order_states:

"to_be_validated"

"to_be_delivered"

"delivered"

***

user_type:

"manager"

"user"

***