<h1 align="center">
  praise
</h1>

## premise
the world divides into 2 categories: handled exceptions and unhandled exceptions\
now let's think about handled exceptions, known points in code that we know might fail for the user, can't do anything about it, just let it die\
but when we do let it die, we want to be able to know what went wrong, but we don't want users to view tracebacks\
how do we make a reporting scheme that is 100% code transparent and will point us to specific known possible failure points in our code?

the idea, given all raises and asserts are statically known sites in our code, is to take a crc32 of the raise node, and map it into a path, scope, and line in our code (this at first sight might sound fragile, but its fragility of change is excatly what we need as we'll soon see).\
the reason this triplet+crc are pretty cool is that given a change in any one of these, we can kind of tell what went wrong even across versions (without even needing to walk through past release commits).
- if the crc changed but nothing else did, the node changed, meaning the kind of exception might have changed, or the text of it
- if the path changed but nothing else did, it means we have the exact same raise on two different places in our code, which might be an opportunity to edit that and make these two sites distinct in our code, in favor of more tolerant error reporing.
- if the scope changed or line number (lineno) changed but nothing else did, it means we moved an the logic around a bit, but it remained fundementally the same.

if we validate and document these changes we can get an error graph that is not only currently true, but is true history wide.\
then, when a user reports a 4 hex digit error code, we can simply look it up in our graph and if it isn't marked `<hash>_old` (just `<hash>`) then we can even goto definition on the result.
