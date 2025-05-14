# Copyright 2025 Stichting Health-RI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace


class OA(DefinedNamespace):
    hasTarget: URIRef # The relationship between an Annotation and its Target.
    hasBody: URIRef # The object of the relationship is a resource that is a body of the Annotation.

    _NS = Namespace("http://www.w3.org/ns/oa#")
