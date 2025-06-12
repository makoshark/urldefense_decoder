> **Note:** *This program effectively disables a security feature universities and companies have adopted. Use this program at your own risk and determine in advance whether it violates your organization's policies to do so!*

These programs read in text converts URLs that have been encoded or "protected" by [Proofpoints URL Defense system](https://www.proofpoint.com/us/resources/data-sheets/essentials-url-defense) into bare (i.e., unprotected) URLs. The URLDefense system modifies incoming emails to replace URLs with encoded URLs that are all proxied or sent first through Proofpoints system.

The system works well for HTML email clients because the visible text of the HTML is typically not changed. But it can be quite anonying with plaintext emails. If you receive email through a company that uses Proofpoint and if you read email using a text-based email client like [Mutt](http://www.mutt.org/) or [Neomutt](https://neomutt.org/). The URLs in the URLDefense-encoded emails are extremely long, and it's often not clear what the URL itself is pointing to until you click through! These scripts clean up the emails for more ergonomic viewing.

I've included two scripts:

1. `urldefense_urldecoder.py` — this decodes the URLs
2. `proofpoint_detagger.py` — this replaces the very large proofpoint tags with "`[WARNING: removed/supressed ProofPoint tag]`"

Once I have put the two files so they are in my execution `$PATH`, I use the following line in my muttrc file:

```
set display_filter="urldefense_urldecoder.py | proofpoint_detagger.py"
```

## Note

`urldefense_urldecoder.py` was written by Eric Van Cleve and [Alex Vlasiuk](vlasiuk.com) and published [a Git gist here](https://gist.github.com/OVlasiuk/7afbbe4fc75e27ed408a332a2b3f2494#file-urldec-py).

`proofpoint_detagger.py` and this repository was built and maintained by [Benjamin Mako Hill](https://mako.cc/).

The programs are licensed under the [GNU General Public License version 3](https://www.gnu.org/licenses/gpl-3.0.en.html).
