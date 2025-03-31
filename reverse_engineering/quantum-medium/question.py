import sys

def exit():
  sys.exit(0)

def scramble(L):
  A = L
  i = 2
  while (i < len(A)):
    A[i-2] += A.pop(i-1)
    A[i-1].append(A[:i-2])
    i += 1
    
  return L

def reverse_scramble(scrambled):
    """
    Attempt to reconstruct the original list of [single_char] sublists
    from the final scrambled structure produced by the 'scramble' function.

    We repeatedly look for an item that has an 'appended prefix' at its end,
    remove that appended reference, and 'un-merge' the single character that
    was appended to its left neighbor. We continue until every top-level item
    is [single_char].

    Assumes 'scrambled' is well-formed and originated from 'scramble'.
    """
    
    def is_single_char_sublist(x):
        """Check if x == [<some single non-list item>]"""
        return (
            isinstance(x, list) and
            len(x) == 1 and
            not isinstance(x[0], list)
        )
    
    # Keep reversing until all top-level items are single-char sublists.
    while not all(is_single_char_sublist(item) for item in scrambled):
        
        # We'll search left->right for an item that still has an 'appended prefix'.
        # By the scramble logic, that appended prefix is always the *last element*
        # of the sublist, and is itself a list (possibly empty) containing references
        # to earlier sublists or an empty list.
        found = False
        
        for idx in range(len(scrambled)):
            item = scrambled[idx]
            if (
                isinstance(item, list) and
                len(item) >= 2 and
                # The last element is the appended prefix (a list).
                isinstance(item[-1], list)
            ):
                # 'item' is the sublist at index idx that had a prefix appended.
                
                # 1) Remove that appended prefix reference
                appended_prefix = item.pop()  # we won't re-insert it as a new item;
                                              # it was just a reference to older sublists.
                
                # 2) The left neighbor is the one that had a single-char appended by +=
                left_idx = idx - 1
                if left_idx < 0:
                    raise ValueError(
                        "Corrupted structure? Found a prefix appended at index 0 with no left neighbor."
                    )
                
                left_item = scrambled[left_idx]
                # left_item had one single char appended at the end
                if not isinstance(left_item, list) or len(left_item) == 0:
                    raise ValueError("Corrupted structure? Left neighbor isn't a list or is empty.")
                
                # 3) Detach the last single char from the left neighbor
                popped_char = left_item.pop()  # e.g. 'B' in the [A,B] example
                # Re-wrap it as a single-character sublist
                new_sublist = [popped_char]
                
                # 4) Re-insert it as a separate top-level item at position idx
                scrambled.insert(idx, new_sublist)
                
                found = True
                break  # We only want to reverse ONE iteration per pass.

        if not found:
            # If we never found any item with an appended prefix,
            # but still not all are single-char sublists, something is inconsistent.
            raise ValueError("No item with appended prefix found, but unscrambling not complete.")
    
    # At this point, everything is [single_char], unscrambled.
    return scrambled


def get_flag():
  flag = open('flag.txt', 'r').read()
  flag = flag.strip()
  hex_flag = []
  for c in flag:
    hex_flag.append([c])

  return hex_flag

def main():
    flag = get_flag()
    cypher = scramble(flag)
    print(f"{len(flag)} {len(cypher)}")
    print(cypher)

    un_cypher = reverse_scramble(cypher)
    print(un_cypher)


if __name__ == '__main__':
  main()