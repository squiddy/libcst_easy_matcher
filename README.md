# libcst_easy_matcher

An experiment to create matchers from source code when working with
[LibCST](https://libcst.readthedocs.io/). A matcher enables you to check
whether a certain node in the tree generated by LibCST matches a certain
pattern.

If I want to check that a statement matches 

```python
client["cookies"] = get_cookie(request)
```

I'd write something like this:

```python
m.Assign(
    targets=[
        m.AssignTarget(
            target=m.Subscript(
                value=m.Attribute(
                    value=m.Name("client"),
                    attr=m.Name("cookies"),
                )
            )
        )
    ],
    value=m.Call(
        func=m.Name(
            value='get_cookie'
        ),
        args=[
            m.Arg(
                value=m.Name(
                    value='request'
                )
            )
        ]
    )
)
```

I'm experimenting here to instead do it like this: 

```python
create_matcher("client['cookies'] = get_cookie(request)")
```

## Placeholders

Just matching against concrete values only get's you so far, so I'm
evaluating the use of placeholders like this:

```python
__ = get_cookie(request)
client[__] = get_cookie(request)
client['cookies'] = __(request)
client['cookies'] = get_cookie(__)
```

All of which should match the example code. `__` might not be the best choice
in the long run, but I needed a valid identifier to be able to still parse
the code with LibCST.

## License

MIT